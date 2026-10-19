"""Validate starter documentation using only the Python standard library."""
from pathlib import Path
import re
import sys

root = Path(__file__).resolve().parents[1]
errors = []
for name in ("README.md", "SECURITY.md", "CONTRIBUTING.md", ".github/CODEOWNERS", "docs/roadmap/12-month-plan.md"):
    if not (root / name).is_file():
        errors.append(f"Missing required file: {name}")
for path in root.rglob("*.md"):
    for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", path.read_text()):
        if "://" in target or target.startswith(("#", "mailto:")):
            continue
        destination = target.split("#", 1)[0]
        if destination and not (path.parent / destination).exists():
            errors.append(f"{path.relative_to(root)}: broken link {target}")
if errors:
    print("\n".join(errors))
    sys.exit(1)
print("Starter documentation checks passed.")
