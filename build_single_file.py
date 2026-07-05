"""build_single_file.py — auto-bundles ALL agent+router Python files into one submission.py"""
import os
import re
import json
import csv
from pathlib import Path
from collections import defaultdict


def read_clean_source(path):
    """Read a .py file, stripping local imports and __future__ using AST."""
    import ast
    content = Path(path).read_text(encoding="utf-8")
    try:
        tree = ast.parse(content)
    except SyntaxError:
        return content # Fallback if there's somehow a syntax error (e.g. from null bytes)
        
    class ImportStripper(ast.NodeTransformer):
        def visit_Import(self, node):
            new_names = [n for n in node.names if not any(n.name.startswith(p) for p in ("agents.", "cb_agents.", "router."))]
            if not new_names:
                return None
            node.names = new_names
            return node
            
        def visit_ImportFrom(self, node):
            if node.module == "__future__":
                return None
            if node.module and any(node.module == p or node.module.startswith(p + ".") for p in ("agents", "cb_agents", "router")):
                # Generate assignments for aliases
                assignments = []
                import ast as std_ast # Use standard ast here inside the transformer
                for alias in node.names:
                    if alias.asname:
                        assignments.append(
                            std_ast.Assign(
                                targets=[std_ast.Name(id=alias.asname, ctx=std_ast.Store())],
                                value=std_ast.Name(id=alias.name, ctx=std_ast.Load())
                            )
                        )
                if assignments:
                    return assignments
                return None
            return node

    class EmptyBlockFixer(ast.NodeTransformer):
        def generic_visit(self, node):
            super().generic_visit(node)
            for field, old_value in ast.iter_fields(node):
                if isinstance(old_value, list) and len(old_value) == 0:
                    if field in ('body', 'orelse', 'finalbody'):
                        # orelse and finalbody are optional and can be empty lists
                        if field == 'body' or (field in ('orelse', 'finalbody') and getattr(node, field) is not None and getattr(node, field) != []):
                            pass # Wait, if orelse is empty list, it's fine. body MUST NOT be empty.
                        if field == 'body':
                            setattr(node, field, [ast.Pass()])
            return node
            
    tree = ImportStripper().visit(tree)
    tree = EmptyBlockFixer().visit(tree)
    ast.fix_missing_locations(tree)
    return ast.unparse(tree)


def _topo_sort(source_files: dict[str, str]) -> list[str]:
    import ast
    all_mods = set(source_files.keys())
    deps: dict[str, set[str]] = defaultdict(set)
    
    for mod_key, filepath in source_files.items():
        content = Path(filepath).read_text(encoding="utf-8")
        try:
            tree = ast.parse(content)
        except SyntaxError:
            continue
        for node in tree.body:
            if isinstance(node, ast.Import):
                for alias in node.names:
                    # Example: import agents.foo
                    parts = alias.name.split('.')
                    if len(parts) >= 2 and parts[0] in ("agents", "cb_agents", "router"):
                        dep_key = f"{parts[0]}/{parts[1]}"
                        if dep_key in all_mods:
                            deps[mod_key].add(dep_key)
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    parts = node.module.split('.')
                    if parts[0] in ("agents", "cb_agents", "router"):
                        if len(parts) >= 2:
                            dep_key = f"{parts[0]}/{parts[1]}"
                        else:
                            # from agents import foo -> foo is the module
                            dep_key = f"{parts[0]}/{node.names[0].name}"
                        if dep_key in all_mods:
                            deps[mod_key].add(dep_key)

    in_degree = {m: 0 for m in all_mods}
    rev: dict[str, set[str]] = defaultdict(set)
    for m in all_mods:
        for dep in deps.get(m, set()):
            if dep in all_mods and dep != m:
                rev[dep].add(m)
                in_degree[m] += 1

    queue = sorted([m for m in all_mods if in_degree[m] == 0])
    order = []
    while queue:
        node = queue.pop(0)
        order.append(node)
        for child in sorted(rev.get(node, set())):
            in_degree[child] -= 1
            if in_degree[child] == 0:
                queue.append(child)
                
    for m in sorted(all_mods):
        if m not in order:
            order.append(m)
    return order


def bundle():
    print("Bundling agent into a single file (auto-discovery)...")

    # 1. Read JSON config files
    skills_dir = Path("skills")

    delegation_map = {}
    delegation_path = skills_dir / "delegation_map.json"
    if delegation_path.exists():
        delegation_map = json.loads(delegation_path.read_text(encoding="utf-8")).get("delegation", {})

    priority_rules = {}
    priority_path = skills_dir / "priority_rules.json"
    if priority_path.exists():
        priority_rules = json.loads(priority_path.read_text(encoding="utf-8"))

    strategy_profiles = {}
    strategy_path = skills_dir / "strategy_profiles.json"
    if strategy_path.exists():
        strategy_profiles = json.loads(strategy_path.read_text(encoding="utf-8"))

    deck_archetypes = {}
    archetypes_path = skills_dir / "deck_archetypes.json"
    if archetypes_path.exists():
        deck_archetypes = json.loads(archetypes_path.read_text(encoding="utf-8"))

    # 2. Read deck EV scores and deck list
    deck_ev = {}
    deck_list = []
    deck_path = Path("staging/deck_new.csv")
    if not deck_path.exists():
        deck_path = Path("submission/deck.csv")
    if not deck_path.exists():
        deck_path = Path("agents/deck_new.csv")
    if deck_path.exists():
        with open(deck_path, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                name = row.get("card_name", "").strip()
                if name:
                    deck_ev[name] = float(row.get("ev_score", 0.0))
                card_id_str = row.get("card_id", "").strip()
                count_str = row.get("count", "").strip()
                if card_id_str and count_str:
                    deck_list.extend([int(card_id_str)] * int(count_str))

    print(f"Loaded {len(deck_ev)} card EV scores, deck has {len(deck_list)} cards")
    if len(deck_list) == 60:
        default_deck_str = repr(deck_list)
    else:
        print(f"Warning: deck has {len(deck_list)} cards, using hardcoded fallback.")
        default_deck_str = repr([
            3, 3, 3, 3, 3, 3, 3, 5, 6, 6,
            11, 19, 19, 65, 66, 304, 305, 676, 676, 676,
            676, 677, 678, 722, 723, 741, 742, 743, 878, 879,
            1079, 1081, 1086, 1086, 1086, 1086, 1102, 1115, 1121, 1122,
            1141, 1142, 1145, 1152, 1152, 1152, 1152, 1171, 1182, 1182,
            1182, 1192, 1219, 1225, 1227, 1227, 1227, 1227, 1231, 1255
        ])

    # 3. Auto-discover ALL .py source files from router/ and agents/
    source_files = {}
    for directory in ["router", "agents"]:
        for py_file in sorted(Path(directory).glob("*.py")):
            if py_file.name == "__init__.py":
                continue
            mod_key = f"{directory}/{py_file.stem}"
            source_files[mod_key] = str(py_file)

    print(f"Discovered {len(source_files)} source modules")

    # 4. Read and clean all sources
    sources: dict[str, str] = {}
    for mod_key, filepath in source_files.items():
        sources[mod_key] = read_clean_source(filepath)

    # 5. Topologically sort based on original source files to find import dependencies
    order = _topo_sort(source_files)
    print(f"Topological order determined for {len(order)} modules")

    # 6. Read the main template
    main_py = read_clean_source("submission/main_template.py")

    # 7. Assemble output
    header = f'''from __future__ import annotations
# Single-file self-contained Pokemon TCG Kaggle Submission Agent
# Auto-generated by build_single_file.py

import json
import logging
import time
import sys
import os
import csv
import math
import random
import hashlib
import datetime
import pathlib
import dataclasses
from pathlib import Path
from typing import Any, Dict, List, Set, Callable, Optional, Tuple
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
from collections import defaultdict

# CRITICAL: Register this module in sys.modules so @dataclass can resolve
# field type annotations. Kaggle loads submissions via importlib.util which
# does NOT auto-register the module, causing dataclasses._is_type() to crash
# with: AttributeError: 'NoneType' object has no attribute '__dict__'
if __name__ not in sys.modules:
    import types as _types
    sys.modules[__name__] = sys.modules.get(__name__) or _types.ModuleType(__name__)

logger = logging.getLogger(__name__)

# ==========================================
# CONSTANTS & EMBEDDED CONFIGURATIONS
# ==========================================

DELEGATION_MAP = {json.dumps(delegation_map, indent=2)}

PRIORITY_RULES = {json.dumps(priority_rules, indent=2)}

STRATEGY_PROFILES = {json.dumps(strategy_profiles, indent=2)}

DECK_ARCHETYPES = {json.dumps(deck_archetypes, indent=2)}

DECK_EV_SCORES = {json.dumps(deck_ev, indent=2)}

DEFAULT_DECK = {default_deck_str}

# Stub for skills path (not available in single-file mode)
_SKILL_PATH = Path("card_metadata.json")

# Monkeypatch Path.mkdir to silently ignore PermissionError/OSError when building log/skills dirs in read-only sandboxes
def _safe_mkdir(self, *args, **kwargs):
    try:
        pathlib.Path._original_mkdir(self, *args, **kwargs)
    except Exception:
        pass

pathlib.Path._original_mkdir = pathlib.Path.mkdir
pathlib.Path.mkdir = _safe_mkdir
'''

    # Build module sections
    module_sections = []
    for mod_key in order:
        src = sources[mod_key]
        # Strip duplicate imports that are already in the header
        cleaned_lines = []
        for line in src.splitlines():
            # Skip standalone stdlib imports already in header
            if re.match(r"^import\s+(json|logging|time|sys|os|csv|math|random|hashlib|datetime|pathlib|dataclasses)\s*$", line):
                continue
            if re.match(r"^from\s+(pathlib|typing|dataclasses|abc|collections)\s+import\s+", line):
                continue
            if re.match(r"^import\s+(random|logging),", line):
                continue
            cleaned_lines.append(line)
        src = "\n".join(cleaned_lines)
        module_sections.append(f"\n# === {mod_key} ===\n{src}")

    all_modules = "\n".join(module_sections)

    # Indent the entire codebase by 4 spaces to place it within a module-level try/except safety net
    indented_modules = ""
    for line in all_modules.splitlines():
        if line.strip():
            indented_modules += "    " + line + "\n"
        else:
            indented_modules += "\n"

    # Assemble output with giant try-except wrap around all classes, functions, and orchestrator init
    output = header + "\n# ==========================================\n# BUNDLED MODULES (TRY/EXCEPT WRAPPED FOR SAFETY)\n# ==========================================\ntry:\n" + indented_modules + f'''
    # Initialize the Orchestrator
    orchestrator = Orchestrator()
    orchestrator.start_game()
except Exception as global_err:
    import logging
    logging.getLogger(__name__).error(f"Global module loading or orchestrator initialization failed: {{global_err}}", exc_info=True)
    orchestrator = None

# ==========================================
# MAIN AGENT INTERFACE
# ==========================================
{main_py}
'''
    
    # Replace all .parent.parent root resolutions to .parent since single-file agent runs from workspace root directly
    output = output.replace(".parent.parent", ".parent")

    # Write both copies
    Path("submission.py").write_text(output, encoding="utf-8")
    Path("submission/submission_single.py").write_text(output, encoding="utf-8")
    print(f"Generated submission.py successfully ({len(output):,} bytes)")


if __name__ == "__main__":
    bundle()
