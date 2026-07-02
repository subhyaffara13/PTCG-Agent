"""Check which cb_agents files use Python 3.10+ syntax without future annotations."""
from pathlib import Path
import re

cb_dir = Path("submission/cb_agents")
for f in sorted(cb_dir.glob("*.py")):
    content = f.read_text(encoding="utf-8")
    has_future = "from __future__ import annotations" in content
    
    # Check for builtin generic type hints: dict[, list[, tuple[, set[
    has_builtin_generics = bool(
        re.search(r":\s*(dict|list|tuple|set)\[", content) or 
        re.search(r"->\s*(dict|list|tuple|set)\[", content)
    )
    
    # Check for pipe union: str | None, int | float, etc.
    has_pipe_union = bool(re.search(r":\s*\w+\s*\|\s*\w+", content) or re.search(r"->\s*\w+\s*\|\s*\w+", content))
    
    if (has_pipe_union or has_builtin_generics) and not has_future:
        issues = []
        if has_pipe_union:
            issues.append("pipe union (X | Y)")
        if has_builtin_generics:
            issues.append("builtin generics (dict[], list[])")
        print("PROBLEM: %s - missing __future__ annotations, uses: %s" % (f.name, ", ".join(issues)))
    elif has_future and (has_pipe_union or has_builtin_generics):
        print("OK (with __future__): %s" % f.name)

# Also check main.py and router files
print("\n--- main.py ---")
content = Path("submission/main.py").read_text(encoding="utf-8")
has_future = "from __future__ import annotations" in content
print("Has __future__: %s" % has_future)
has_310 = bool(re.search(r":\s*(dict|list|tuple|set)\[", content) or re.search(r":\s*\w+\s*\|\s*\w+", content))
print("Has 3.10+ syntax: %s" % has_310)

print("\n--- router/ ---")
for f in sorted(Path("submission/router").glob("*.py")):
    content = f.read_text(encoding="utf-8")
    has_future = "from __future__ import annotations" in content
    has_310 = bool(
        re.search(r":\s*(dict|list|tuple|set)\[", content) or 
        re.search(r"->\s*(dict|list|tuple|set)\[", content) or
        re.search(r":\s*\w+\s*\|\s*\w+", content) or
        re.search(r"->\s*\w+\s*\|\s*\w+", content)
    )
    if has_310 and not has_future:
        print("PROBLEM: %s" % f.name)
    elif has_310:
        print("OK (with __future__): %s" % f.name)
