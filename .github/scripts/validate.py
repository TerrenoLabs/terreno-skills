"""Basic repo checks: manifests parse, plugin sources exist, SKILL.md frontmatter is valid."""
import json, pathlib, re, sys

root = pathlib.Path(__file__).resolve().parents[2]
errors = []

for manifest in [
    ".claude-plugin/marketplace.json",
    ".cursor-plugin/marketplace.json",
    ".agents/plugins/marketplace.json",
    "skills.sh.json",
    *[str(p.relative_to(root)) for p in root.glob("plugins/*/.*-plugin/plugin.json")],
]:
    path = root / manifest
    try:
        json.loads(path.read_text())
    except Exception as error:
        errors.append(f"{manifest}: {error}")

for manifest, key in [
    (".claude-plugin/marketplace.json", None),
    (".cursor-plugin/marketplace.json", None),
    (".agents/plugins/marketplace.json", "path"),
]:
    data = json.loads((root / manifest).read_text())
    for plugin in data["plugins"]:
        src = plugin["source"]
        src = src[key] if isinstance(src, dict) else src
        base = root if manifest != ".cursor-plugin/marketplace.json" else root / "plugins"
        if not (base / src).resolve().is_dir():
            errors.append(f"{manifest}: source {src!r} for {plugin['name']} not found")

skills = list(root.glob("plugins/*/skills/*/SKILL.md")) + list(root.glob("skills/*/SKILL.md"))
if not skills:
    errors.append("no SKILL.md files found")
for skill in skills:
    rel = skill.relative_to(root)
    match = re.match(r"^---\n(.*?)\n---\n", skill.read_text(), re.S)
    if not match:
        errors.append(f"{rel}: missing frontmatter")
        continue
    front = match.group(1)
    if not re.search(r"^name:\s*\S", front, re.M) or not re.search(r"^description:\s*\S", front, re.M):
        errors.append(f"{rel}: frontmatter needs name and description")

print(f"checked {len(skills)} skills")
if errors:
    print("\n".join(errors))
    sys.exit(1)
