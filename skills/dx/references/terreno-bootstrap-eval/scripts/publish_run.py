#!/usr/bin/env python3
"""Upload a bootstrap eval run to the results repository and compare runs.

    publish_run.py <run-dir> --repo OWNER/NAME     upload the app and the eval folder
    publish_run.py <run-dir> --repo OWNER/NAME --results-only   the eval folder only; rerun without it to add the app
    publish_run.py ci <run-dir> --repo OWNER/NAME  record the app commit's CI results
    publish_run.py compare --repo OWNER/NAME       newest run per version vs the previous version

Layout in the results repository:

    branch runs/<run id>      the generated app with its per-stage history
    branch v<major>.<minor>   points at the newest run for that version
    master: results/<major>.<minor>/<run id>/   run.json, timings.json, scores/, static/, evidence/
    master: results/index.json, results/README.md   rebuilt on every publish

Needs git and an authenticated gh. Publishing refuses an app with a committed
.env file or a secret-shaped value.
"""
import argparse
import json
import pathlib
import re
import shutil
import subprocess
import sys
import tempfile

SECRET_PATTERNS = [
    re.compile(r"sk-[A-Za-z0-9_-]{20,}"),
    re.compile(r"AIza[0-9A-Za-z_-]{30,}"),
    re.compile(r"gh[pousr]_[A-Za-z0-9]{30,}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"(?i)\b(BETTER_AUTH_SECRET|TOKEN_SECRET|SESSION_SECRET|REFRESH_TOKEN_SECRET|INITIAL_ADMIN_PASSWORD)[ \t]*[=:][ \t]*[\"']?(?=[^\s\"']*\d)(?=[^\s\"']*[a-z])[A-Za-z0-9+/=_-]{16,}"),
]
# The app repository has no remote of its own, so pushes borrow gh's credentials.
GH_AUTH = ("-c", "credential.helper=!gh auth git-credential")
REGRESSION_POINTS = 10
REGRESSION_TIME = 1.5


def run(*args, cwd=None, capture=False, check=True):
    result = subprocess.run([str(a) for a in args], cwd=cwd, text=True, capture_output=capture)
    if check and result.returncode != 0:
        sys.exit(f"command failed: {' '.join(str(a) for a in args)}\n{result.stderr or ''}")
    return result.stdout.strip() if capture else result.returncode


def load_json(path, default=None):
    try:
        return json.loads(pathlib.Path(path).read_text())
    except (OSError, json.JSONDecodeError):
        return default


def minor_of(version):
    match = re.match(r"^(\d+)\.(\d+)", version)
    if not match:
        sys.exit(f"cannot read major.minor from version {version!r}")
    return f"{match.group(1)}.{match.group(2)}"


def version_key(minor):
    return tuple(int(part) for part in minor.split("."))


def local_secret_values(app):
    """Values from the app's gitignored .env files: the secrets this run really uses."""
    values = set()
    for env_file in app.rglob(".env*"):
        if "node_modules" in env_file.parts or env_file.name.endswith(".example") or not env_file.is_file():
            continue
        for line in env_file.read_text(errors="ignore").splitlines():
            key, _, value = line.partition("=")
            value = value.strip().strip("\"'")
            if re.search(r"(?i)secret|password|key|token", key) and len(value) >= 12:
                values.add(value)
    return values


def scan_for_secrets(app):
    """Refuse committed env files, any real local secret, and secret-shaped values outside tests."""
    tracked = run("git", "ls-files", cwd=app, capture=True).splitlines()
    real = local_secret_values(app)
    problems = []
    for rel in tracked:
        path = app / rel
        if path.name == ".env" or re.fullmatch(r"\.env\.(local|production|development)", path.name):
            problems.append(f"{rel}: env file is committed")
            continue
        if not path.is_file() or path.stat().st_size > 400_000:
            continue
        body = path.read_text(errors="ignore")
        if any(value in body for value in real):
            problems.append(f"{rel}: contains a value from a local .env file")
            continue
        if re.search(r"\.(test|spec)\.[jt]sx?$", rel):
            continue
        for pattern in SECRET_PATTERNS:
            if pattern.search(body):
                problems.append(f"{rel}: matches {pattern.pattern[:40]}")
                break
    return problems


def clone(repo, workdir):
    target = pathlib.Path(workdir) / "results"
    run("gh", "repo", "clone", repo, target, "--", "--quiet")
    if run("git", "rev-parse", "--verify", "--quiet", "HEAD", cwd=target, check=False, capture=True) == "":
        run("git", "checkout", "-b", "master", cwd=target)
    return target


def stage_summary(run_dir_published):
    timings = load_json(run_dir_published / "timings.json", {"stages": {}})["stages"]
    stages = {}
    for score_file in sorted((run_dir_published / "scores").glob("*.json")):
        score = load_json(score_file, {})
        name = score_file.stem
        if name == "overall":
            continue
        attempts = [a for a in timings.get(name, []) if "minutes" in a]
        stages[name] = {
            "status": score.get("status"),
            "score": score.get("score"),
            "passMark": score.get("passMark"),
            "minutes": attempts[0]["minutes"] if attempts else None,
            "attempts": len(attempts),
        }
    return stages


def rebuild_index(results):
    entries = []
    for run_json in sorted(results.glob("*/*/run.json")):
        folder = run_json.parent
        meta = load_json(run_json, {})
        overall = load_json(folder / "scores" / "overall.json", {})
        stages = stage_summary(folder)
        minutes = [s["minutes"] for s in stages.values() if s["minutes"] is not None]
        entries.append({
            "version": meta.get("version"),
            "minor": folder.parent.name,
            "runId": folder.name,
            "prompt": meta.get("prompt"),
            "appBranch": meta.get("appBranch"),
            "appSha": meta.get("appSha"),
            "overallScore": overall.get("overallScore"),
            "closeness": overall.get("closeness"),
            "totalMinutes": round(sum(minutes), 1) if minutes else None,
            "ci": load_json(folder / "ci.json"),
            "stages": stages,
        })
    entries.sort(key=lambda e: (version_key(e["minor"]), e["runId"]))
    (results / "index.json").write_text(json.dumps({"runs": entries}, indent=2) + "\n")
    lines = [
        "# Bootstrap eval runs",
        "",
        "Generated by `terreno-bootstrap-eval`. One row per run; the app is on the linked branch.",
        "",
        "| Version | Run | Score | Closeness | Minutes | Failing or blocked stages | App |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for entry in reversed(entries):
        weak = [f"{name} ({s['status']})" for name, s in entry["stages"].items() if s["status"] != "pass"]
        lines.append(
            f"| {entry['version']} | [{entry['runId']}]({entry['minor']}/{entry['runId']}/) | "
            f"{entry['overallScore']} | {entry['closeness']} | {entry['totalMinutes']} | "
            f"{', '.join(weak) or 'none'} | {('`' + entry['appBranch'] + '`') if entry['appBranch'] else 'not uploaded'} |"
        )
    (results / "README.md").write_text("\n".join(lines) + "\n")
    return entries


def app_root(run_dir):
    """The app is <run>/app, or the one directory the scaffold CLI made inside it."""
    app = run_dir / "app"
    if (app / ".git").exists():
        return app
    nested = [child for child in app.iterdir() if (child / ".git").exists()]
    if len(nested) != 1:
        sys.exit(f"expected one git repository in {app}, found {len(nested)}")
    return nested[0]


def publish(run_dir, repo, results_only=False):
    """Push the app branch and the results. With results_only, push the results
    alone (for example when the token cannot push workflow files yet); run the
    full publish later to add the app branch."""
    app, eval_dir = app_root(run_dir), run_dir / "eval"
    meta = load_json(eval_dir / "run.json")
    if not meta or not meta.get("version") or not meta.get("runId"):
        sys.exit("eval/run.json needs version and runId")
    minor = minor_of(meta["version"])
    branch, pointer = f"runs/{meta['runId']}", f"v{minor}"
    sha = run("git", "rev-parse", "HEAD", cwd=app, capture=True)

    if results_only:
        meta.update({"appBranch": None, "appSha": sha, "versionBranch": None})
    else:
        problems = scan_for_secrets(app)
        if problems:
            sys.exit("refusing to publish, the app has committed secrets:\n  " + "\n  ".join(problems))
        if run("git", "status", "--porcelain", cwd=app, capture=True):
            sys.exit("refusing to publish: the app has uncommitted changes")
        url = f"https://github.com/{repo}.git"
        run("git", *GH_AUTH, "push", "--quiet", url, f"HEAD:refs/heads/{branch}", cwd=app)
        run("git", *GH_AUTH, "push", "--quiet", "--force", url, f"HEAD:refs/heads/{pointer}", cwd=app)
        meta.update({"appBranch": branch, "appSha": sha, "versionBranch": pointer})
    (eval_dir / "run.json").write_text(json.dumps(meta, indent=2) + "\n")

    with tempfile.TemporaryDirectory() as workdir:
        target = clone(repo, workdir)
        dest = target / "results" / minor / meta["runId"]
        if dest.exists():
            shutil.rmtree(dest)
        shutil.copytree(eval_dir, dest, ignore=shutil.ignore_patterns("scratch", "*.log", "node_modules"))
        rebuild_index(target / "results")
        run("git", "add", "results", cwd=target)
        run("git", "commit", "--quiet", "-m", f"Add bootstrap eval run {meta['runId']}", cwd=target)
        run("git", "push", "--quiet", "origin", "HEAD:master", cwd=target)
    if not results_only:
        print(f"app:     https://github.com/{repo}/tree/{branch} ({sha[:8]})")
    print(f"results: https://github.com/{repo}/tree/master/results/{minor}/{meta['runId']}")


def record_ci(run_dir, repo):
    meta = load_json(run_dir / "eval" / "run.json") or {}
    sha = meta.get("appSha")
    if not sha:
        sys.exit("publish the run first: eval/run.json has no appSha")
    raw = run("gh", "api", f"repos/{repo}/commits/{sha}/check-runs", "--paginate", capture=True)
    checks = [
        {"name": c["name"], "status": c["status"], "conclusion": c["conclusion"], "url": c["html_url"]}
        for c in json.loads(raw).get("check_runs", [])
    ]
    pending = [c for c in checks if c["status"] != "completed"]
    summary = {
        "sha": sha,
        "checks": checks,
        "complete": bool(checks) and not pending,
        "green": bool(checks) and not pending and all(c["conclusion"] in ("success", "skipped", "neutral") for c in checks),
    }
    (run_dir / "eval" / "ci.json").write_text(json.dumps(summary, indent=2) + "\n")
    if pending or not checks:
        print(f"{len(pending)} of {len(checks)} checks still running; run again later")
        return
    minor = minor_of(meta["version"])
    with tempfile.TemporaryDirectory() as workdir:
        target = clone(repo, workdir)
        dest = target / "results" / minor / meta["runId"]
        dest.mkdir(parents=True, exist_ok=True)
        shutil.copy(run_dir / "eval" / "ci.json", dest / "ci.json")
        rebuild_index(target / "results")
        run("git", "add", "results", cwd=target)
        if run("git", "diff", "--cached", "--quiet", cwd=target, check=False) != 0:
            run("git", "commit", "--quiet", "-m", f"Record CI for {meta['runId']}", cwd=target)
            run("git", "push", "--quiet", "origin", "HEAD:master", cwd=target)
    print(f"CI {'green' if summary['green'] else 'RED'}: " + ", ".join(f"{c['name']}={c['conclusion']}" for c in checks))


def compare(repo):
    raw = run("gh", "api", f"repos/{repo}/contents/results/index.json", "-H", "Accept: application/vnd.github.raw", capture=True)
    runs = json.loads(raw)["runs"]
    latest = {}
    for entry in runs:
        latest[entry["minor"]] = entry
    minors = sorted(latest, key=version_key)
    if len(minors) < 2:
        print(f"only {len(minors)} version published; nothing to compare yet")
        return
    regressions = []
    for previous_minor, current_minor in zip(minors, minors[1:]):
        previous, current = latest[previous_minor], latest[current_minor]
        print(f"\n{previous['version']} -> {current['version']}: "
              f"score {previous['overallScore']} -> {current['overallScore']}, "
              f"minutes {previous['totalMinutes']} -> {current['totalMinutes']}")
        print(f"{'stage':<16}{'score':>14}{'minutes':>16}  status")
        for name, now in current["stages"].items():
            before = previous["stages"].get(name, {})
            flags = []
            if before.get("status") == "pass" and now["status"] != "pass":
                flags.append(f"{before['status']} -> {now['status']}")
            if None not in (before.get("score"), now["score"]) and before["score"] - now["score"] >= REGRESSION_POINTS:
                flags.append("score drop")
            if before.get("minutes") and now["minutes"] and now["minutes"] >= before["minutes"] * REGRESSION_TIME:
                flags.append("slower")
            print(f"{name:<16}{str(before.get('score')) + ' -> ' + str(now['score']):>14}"
                  f"{str(before.get('minutes')) + ' -> ' + str(now['minutes']):>16}  "
                  f"{now['status']}{'  REGRESSION: ' + ', '.join(flags) if flags else ''}")
            if flags:
                regressions.append(f"{current['version']} {name}: {', '.join(flags)}")
    print("\nregressions:" if regressions else "\nno regressions")
    for line in regressions:
        print(f"  - {line}")


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawTextHelpFormatter)
    parser.add_argument("args", nargs="+")
    parser.add_argument("--repo", required=True)
    parser.add_argument("--results-only", action="store_true", help="upload the eval folder without the app branch")
    parsed = parser.parse_args()
    command, rest = parsed.args[0], parsed.args[1:]
    if command == "compare":
        compare(parsed.repo)
    elif command == "ci":
        if not rest:
            sys.exit("usage: publish_run.py ci <run-dir> --repo OWNER/NAME")
        record_ci(pathlib.Path(rest[0]).resolve(), parsed.repo)
    else:
        publish(pathlib.Path(command).resolve(), parsed.repo, results_only=parsed.results_only)


if __name__ == "__main__":
    main()
