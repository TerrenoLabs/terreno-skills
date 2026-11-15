#!/usr/bin/env python3
"""Cheap file and grep checks on a bootstrapped app, as leads for the scorer.

    static_checks.py <app-dir> [--stage <stage>] [--out <file>]

These checks prove nothing about behavior. They tell the scorer where to look
and catch the obvious (a missing checklist, a committed secret) in seconds.
Exit code is always 0; read the report.
"""
import argparse
import json
import pathlib
import re
import subprocess

SKIP_DIRS = {"node_modules", ".git", "dist", ".expo", "coverage", "build", ".skills", ".agents", ".claude"}
TEXT_SUFFIXES = {".ts", ".tsx", ".js", ".json", ".jsonc", ".yml", ".yaml", ".md", ".toml", ".example", ""}
STAGES = [
    "scaffold", "feature", "auth", "roles", "admin", "theme", "ai", "consent",
    "flags", "tests-ci", "agent-tooling", "deploy", "handoff",
]
SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"AIza[0-9A-Za-z_-]{30,}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"(?i)\b(BETTER_AUTH_SECRET|TOKEN_SECRET|SESSION_SECRET|REFRESH_TOKEN_SECRET|INITIAL_ADMIN_PASSWORD)[ \t]*[=:][ \t]*[\"']?(?=[^\s\"']*\d)(?=[^\s\"']*[a-z])[A-Za-z0-9+/=_-]{16,}"),
]


def tracked_files(app):
    """Committed files only: gitignored .env files are allowed to hold secrets."""
    try:
        out = subprocess.run(
            ["git", "-C", str(app), "ls-files"], capture_output=True, text=True, check=True
        ).stdout
        files = [app / line for line in out.splitlines() if line]
    except (subprocess.CalledProcessError, FileNotFoundError):
        files = [p for p in app.rglob("*") if p.is_file()]
    return [
        f for f in files
        if f.is_file() and not SKIP_DIRS.intersection(f.relative_to(app).parts)
    ]


def read(path):
    try:
        return path.read_text(errors="ignore")
    except OSError:
        return ""


class App:
    def __init__(self, root):
        self.root = root
        self.files = tracked_files(root)
        self._text = {}

    def text(self, path):
        if path not in self._text:
            suffix_ok = path.suffix in TEXT_SUFFIXES or path.name.startswith(".env")
            self._text[path] = read(path) if suffix_ok and path.stat().st_size < 400_000 else ""
        return self._text[path]

    def has(self, rel):
        return (self.root / rel).exists()

    def glob(self, pattern):
        return [f for f in self.files if f.relative_to(self.root).match(pattern)]

    def grep(self, pattern, under="", suffixes=(".ts", ".tsx")):
        regex = re.compile(pattern)
        hits = []
        for f in self.files:
            rel = f.relative_to(self.root).as_posix()
            if not rel.startswith(under) or (suffixes and f.suffix not in suffixes):
                continue
            for number, line in enumerate(self.text(f).splitlines(), 1):
                if regex.search(line):
                    hits.append(f"{rel}:{number}")
                    break
        return hits


def check(name, ok, detail=""):
    return {"check": name, "ok": bool(ok), "detail": detail if isinstance(detail, str) else ", ".join(detail[:5])}


def state(app):
    path = app.root / ".terreno" / "bootstrap.json"
    if not path.exists():
        return {}
    try:
        return json.loads(path.read_text())
    except json.JSONDecodeError:
        return {}


def scaffold(app):
    data = state(app)
    return [
        check("backend/ and frontend/ exist", app.has("backend/package.json") and app.has("frontend/package.json")),
        check("state file has terrenoVersion", bool(data.get("terrenoVersion")), str(data.get("terrenoVersion", ""))),
        check("state file records the request verbatim", bool(data.get("request"))),
    ]


def feature(app):
    models = app.grep(r"syncPlugin", "backend/src/models")
    raw_fetch = app.grep(r"\b(fetch|axios)\s*[.(]", "frontend/app") + app.grep(r"\b(fetch|axios)\s*[.(]", "frontend/components")
    express = app.grep(r"\b(app|router)\.(get|post|patch|put|delete)\(", "backend/src/api")
    return [
        check("a synced model exists", models, models),
        check("modelRouter with sync config", app.grep(r"sync:\s*\{", "backend/src")),
        check("synced hooks used in screens", app.grep(r"useQuery|useMutate", "frontend")),
        check("no raw fetch/axios in screens", not raw_fetch, raw_fetch),
        check("no hand-written Express routes in api/", not express, express),
        check("testIDs present in screens", app.grep(r"testID=", "frontend/app")),
    ]


def auth(app):
    leaks = []
    for f in app.files:
        if f.name == ".env.example" or f.suffix == ".md":
            continue
        body = app.text(f)
        if any(p.search(body) for p in SECRET_PATTERNS):
            leaks.append(f.relative_to(app.root).as_posix())
    committed_env = [f.relative_to(app.root).as_posix() for f in app.files if f.name == ".env"]
    return [
        check("no .env committed", not committed_env, committed_env),
        check("no secret-shaped values committed", not leaks, leaks),
        check("rate limit not disabled outside tests", not app.grep(r"rateLimit:\s*false", "backend/src/server"), ""),
        check("reset-password screen exists", app.glob("frontend/app/**/*eset*assword*") or app.glob("frontend/app/*eset*assword*")),
        check("seed guards production", app.grep(r"production", "backend/src/scripts")),
    ]


def roles(app):
    return [
        check("roles defined in access module", app.grep(r"roles?", "backend/src/access")),
        check("a role other than admin is named", app.grep(r"[\"'](operator|manager|member|editor|support|viewer)[\"']", "backend/src")),
        check("a test mentions 403", app.grep(r"403", "backend/src", suffixes=(".ts",))),
    ]


def admin(app):
    return [
        check("AdminApp registered", app.grep(r"AdminApp", "backend/src")),
        check("admin screens exist", app.glob("frontend/app/**/admin/*")),
        check("admin gate in frontend", app.grep(r"canOpenAdminPage|\.admin\b", "frontend/app")),
    ]


def theme(app):
    hexes = [h for h in app.grep(r"#[0-9a-fA-F]{6}\b", "frontend/app") + app.grep(r"#[0-9a-fA-F]{6}\b", "frontend/components")]
    shots = [f for f in app.glob("docs/bootstrap/theme/*") if f.suffix in {".png", ".jpg", ".webp"}]
    return [
        check("theme primitives customized", app.grep(r"primary\d{3}|setPrimitives|primitives", "frontend/constants")),
        check("no hex colors in screens", not hexes, hexes),
        check("responsive props or breakpoints used", app.grep(r"\b(sm|md|lg|xl)[A-Z][a-zA-Z]+=|isSupportedDesktopWidth|mediaQuery", "frontend")),
        check("color scheme selectable", app.grep(r"setColorScheme|themeColorSchemeOptions", "frontend")),
        check("12 theme screenshots", len(shots) >= 12, f"{len(shots)} found"),
    ]


def ai(app):
    return [
        check("@terreno/ai in backend deps", "@terreno/ai" in read(app.root / "backend/package.json")),
        check("AI service or app registered", app.grep(r"AiApp|AIService|addGptRoutes", "backend/src")),
        check("chat screen uses GPTChat", app.grep(r"GPTChat", "frontend")),
        check("a tool is defined", app.grep(r"\btools?\b\s*[:=]", "backend/src")),
        check("mock-model test exists", app.grep(r"doGenerate|doStream|MockLanguageModel", "backend/src")),
    ]


def consent(app):
    return [
        check("consent wired in backend", app.grep(r"[Cc]onsent", "backend/src")),
        check("consent gate in frontend", app.grep(r"[Cc]onsent", "frontend/app")),
        check("terms and privacy seeded", app.grep(r"(?i)terms", "backend/src/scripts") and app.grep(r"(?i)privacy", "backend/src/scripts")),
    ]


def flags(app):
    return [
        check("flags used on the server", app.grep(r"[Ff]eatureFlag|[Ff]lags?App", "backend/src")),
        check("flags read in the client", app.grep(r"useFeatureFlags|useTerrenoFeatureFlags", "frontend")),
    ]


def tests_ci(app):
    workflows = app.glob(".github/workflows/*.yml") + app.glob(".github/workflows/*.yaml")
    workflow_text = "\n".join(app.text(f) for f in workflows)
    configs = "\n".join(read(app.root / p) for p in (
        "backend/bunfig.toml", "frontend/bunfig.toml", "backend/package.json", "frontend/package.json",
        "frontend/jest.config.js", "frontend/jest.config.ts",
    ))
    return [
        check("backend tests exist", app.glob("backend/src/**/*.test.ts") or app.glob("backend/**/*.test.ts")),
        check("frontend tests exist", app.glob("frontend/**/*.test.ts*")),
        check("playwright spec exists", app.glob("frontend/e2e/*.spec.ts") or app.glob("e2e/*.spec.ts")),
        check("coverage threshold configured", re.search(r"coverageThreshold|coverage-threshold", configs)),
        check("workflows run coverage", "coverage" in workflow_text, f"{len(workflows)} workflows"),
        check("workflows validate secrets", "Missing required secrets" in workflow_text or "secrets." not in workflow_text),
        check(".circleci/config.yml exists", app.has(".circleci/config.yml")),
    ]


def agent_tooling(app):
    claude = read(app.root / "CLAUDE.md")
    skills = [f for f in app.root.glob("**/SKILL.md") if "node_modules" not in f.parts]
    return [
        check(".mcp.json committed", app.has(".mcp.json")),
        check("CLAUDE.md and AGENTS.md exist", app.has("CLAUDE.md") and app.has("AGENTS.md")),
        check("CLAUDE.md names test commands", re.search(r"bun (run )?test", claude)),
        check("Terreno skills installed", len(skills) >= 5, f"{len(skills)} SKILL.md files"),
    ]


def deploy(app):
    workflows = [f.name for f in app.glob(".github/workflows/*") if re.search(r"deploy", f.name)]
    data = state(app).get("stages", {}).get("deploy", {})
    return [
        check("Dockerfile exists", app.has("Dockerfile")),
        check("deploy workflow exists", workflows, workflows),
        check("state records a URL or a blocked reason", data.get("status") == "pass" and "http" in json.dumps(data) or data.get("status") == "blocked" and data.get("reason"), json.dumps(data)[:200]),
    ]


def handoff(app):
    checklist = read(app.root / "CHECKLIST.md")
    sections = len(re.findall(r"^## ", checklist, re.M))
    boxes = len(re.findall(r"^- \[[ x]\]", checklist, re.M))
    data = state(app).get("stages", {})
    return [
        check("CHECKLIST.md at root", bool(checklist)),
        check("checklist has a section per stage", sections >= len(STAGES), f"{sections} sections, {boxes} checkboxes"),
        check("checklist names the initial user", re.search(r"(?i)initial (admin|user)", checklist)),
        check("checklist has 'Before real users'", re.search(r"(?i)before real users", checklist)),
        check("initial admin seeded from env", app.grep(r"INITIAL_ADMIN_EMAIL", "backend/src")),
        check("initial password not committed", not app.grep(r"INITIAL_ADMIN_PASSWORD\s*=\s*\S{6,}", "", suffixes=())),
        check("every stage has a state entry", all(s in data for s in STAGES), [s for s in STAGES if s not in data]),
    ]


CHECKS = {
    "scaffold": scaffold, "feature": feature, "auth": auth, "roles": roles, "admin": admin,
    "theme": theme, "ai": ai, "consent": consent, "flags": flags, "tests-ci": tests_ci,
    "agent-tooling": agent_tooling, "deploy": deploy, "handoff": handoff,
}


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("app", type=pathlib.Path)
    parser.add_argument("--stage", choices=STAGES)
    parser.add_argument("--out", type=pathlib.Path)
    args = parser.parse_args()
    app = App(args.app.resolve())
    stages = [args.stage] if args.stage else STAGES
    report = {"app": str(app.root), "state": state(app).get("stages", {}), "stages": {s: CHECKS[s](app) for s in stages}}
    body = json.dumps(report, indent=2) + "\n"
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(body)
    for stage in stages:
        results = report["stages"][stage]
        print(f"{stage}: {sum(r['ok'] for r in results)}/{len(results)}")
        for result in results:
            if not result["ok"]:
                print(f"  - {result['check']}" + (f" ({result['detail']})" if result["detail"] else ""))


if __name__ == "__main__":
    main()
