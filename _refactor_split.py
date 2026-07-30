"""Split large Python files into ~50-line packages with proper cross-references."""
import ast
import builtins
import shutil
from pathlib import Path

ROOT = Path(r"C:\Users\subhy\.gemini\antigravity\scratch\ptcg-agent")
TARGET = 50

BUILTIN_NAMES = set(dir(builtins))

def _is_name_main_check(node):
    """Check if an ast.If tests __name__ == '__main__'."""
    if not isinstance(node, ast.If):
        return False
    return (isinstance(node.test, ast.Compare)
            and isinstance(node.test.left, ast.Name) and node.test.left.id == '__name__'
            and len(node.test.ops) == 1 and isinstance(node.test.ops[0], ast.Eq)
            and len(node.test.comparators) == 1
            and isinstance(node.test.comparators[0], ast.Constant)
            and node.test.comparators[0].value == '__main__')

def _names_from_node(node):
    if isinstance(node, ast.Import):
        for alias in node.names:
            yield alias.asname or alias.name.split('.')[0]
    elif isinstance(node, ast.ImportFrom):
        for alias in node.names:
            yield alias.asname or alias.name
    elif isinstance(node, ast.Assign):
        for target in node.targets:
            if isinstance(target, ast.Name):
                yield target.id
            elif isinstance(target, (ast.List, ast.Tuple)):
                for elt in target.elts:
                    if isinstance(elt, ast.Name):
                        yield elt.id
    elif isinstance(node, ast.AnnAssign):
        if isinstance(node.target, ast.Name):
            yield node.target.id
    elif isinstance(node, ast.AugAssign):
        if isinstance(node.target, ast.Name):
            yield node.target.id
    elif isinstance(node, ast.Try):
        for child in node.body:
            yield from _names_from_node(child)
        for handler in node.handlers:
            for child in handler.body:
                yield from _names_from_node(child)
    elif isinstance(node, ast.If) and not _is_name_main_check(node):
        for child in node.body:
            yield from _names_from_node(child)

def _func_param_names(node):
    """Get parameter names from a FunctionDef node."""
    names = set()
    names.update(a.arg for a in node.args.args)
    names.update(a.arg for a in node.args.kwonlyargs)
    if node.args.vararg: names.add(node.args.vararg.arg)
    if node.args.kwarg: names.add(node.args.kwarg.arg)
    return names

def get_local_names(node):
    """Collect locally-defined names (params, nested defs) for a function or class."""
    names = set()
    if isinstance(node, ast.FunctionDef):
        names |= _func_param_names(node)
    if isinstance(node, ast.ClassDef):
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                names.add(item.name)
                names |= _func_param_names(item)
            elif isinstance(item, ast.ClassDef):
                names.add(item.name)
    return names

def get_body_refs_for_funcs(source, func_names):
    tree = ast.parse(source)
    refs = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)) and node.name in func_names:
            local_names = get_local_names(node)
            for sub in ast.walk(node):
                if isinstance(sub, ast.Name) and sub.id not in BUILTIN_NAMES and sub.id not in local_names:
                    refs.add(sub.id)
    return refs

def refactor_file(filepath):
    filepath = Path(filepath)
    with open(filepath, encoding='utf-8') as f:
        source = f.read()
    lines = source.splitlines(keepends=True)
    total = len(lines)
    if total <= 100:
        return False

    name = filepath.name
    print(f"  {name} ({total} lines)...", end='')

    tree = ast.parse(source)

    shared_nodes = []
    def_nodes = []
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            def_nodes.append(node)
        else:
            shared_nodes.append(node)

    if not def_nodes:
        print(" -> no defs, skipping")
        return False

    defs_with_text = []
    for node in def_nodes:
        text = ''.join(lines[node.lineno-1:node.end_lineno])
        defs_with_text.append((node, node.name, node.lineno-1, node.end_lineno, text))

    groups = []
    current, cur_size = [], 0
    for d in defs_with_text:
        size = d[3] - d[2]
        if cur_size + size > TARGET and current:
            groups.append(current)
            current, cur_size = [d], size
        else:
            current.append(d)
            cur_size += size
    if current:
        groups.append(current)

    if len(groups) <= 1:
        print(" -> only 1 group, skipping")
        return False

    all_def_names = set(d[1] for d in defs_with_text)

    name_to_group = {}
    for i, g in enumerate(groups):
        for d in g:
            name_to_group[d[1]] = i

    # Separate shared nodes: pre-import (no def refs) vs post-import (references defs)
    pre_import_nodes = []
    post_import_nodes = []
    for node in shared_nodes:
        refs_def = False
        for sub in ast.walk(node):
            if isinstance(sub, ast.Name) and sub.id in all_def_names:
                refs_def = True
                break
        if refs_def:
            post_import_nodes.append(node)
        else:
            pre_import_nodes.append(node)

    # Build pre-import names
    pre_import_names = set()
    for node in pre_import_nodes:
        for n in _names_from_node(node):
            pre_import_names.add(n)

    # Post-import names (defined in _setup)
    post_import_names = set()
    for node in post_import_nodes:
        for n in _names_from_node(node):
            post_import_names.add(n)

    pkg_dir = filepath.with_suffix('')
    pkg_dir.mkdir(exist_ok=True)
    shutil.copy2(filepath, str(filepath) + '.bak')

    file_parts = []
    for i, group in enumerate(groups):
        names = [d[1] for d in group if d[1] is not None]
        pn = names[0] if len(names) == 1 else '_'.join(names[:3])
        pn = ''.join(c for c in pn if c.isalnum() or c == '_').lower()[:60]
        if not pn or pn[0].isdigit():
            pn = f"part_{i+1:02d}"

        func_names_set = set(d[1] for d in group if d[1] is not None)
        refs = get_body_refs_for_funcs(source, func_names_set)

        shared_needed = set()
        cross_needed = {}
        setup_needed = set()

        for ref in refs:
            if ref in pre_import_names:
                shared_needed.add(ref)
            elif ref in post_import_names:
                setup_needed.add(ref)
            elif ref in all_def_names:
                rg = name_to_group.get(ref)
                if rg is not None and rg != i:
                    other_group = groups[rg]
                    other_names = [od[1] for od in other_group if od[1] is not None]
                    other_pn = other_names[0] if len(other_names) == 1 else '_'.join(other_names[:3])
                    other_pn = ''.join(c for c in other_pn if c.isalnum() or c == '_').lower()[:60]
                    cross_needed[ref] = other_pn

        part_lines = []
        if shared_needed:
            part_lines.append(f"from . import {', '.join(sorted(shared_needed))}\n")
        if setup_needed:
            part_lines.append(f"from ._setup import {', '.join(sorted(setup_needed))}\n")
        if cross_needed:
            mod_to_names = {}
            for n, mod in cross_needed.items():
                mod_to_names.setdefault(mod, []).append(n)
            for mod, nms in sorted(mod_to_names.items()):
                part_lines.append(f"from .{mod} import {', '.join(sorted(nms))}\n")
        if part_lines:
            part_lines.append('\n')

        for d in group:
            part_lines.append(d[4].rstrip() + '\n\n')

        (pkg_dir / f"{pn}.py").write_text(''.join(part_lines), encoding='utf-8')
        file_parts.append((pn, [d[1] for d in group if d[1] is not None]))

    # Write _setup.py for post-import code
    has_setup = bool(post_import_nodes)
    if has_setup:
        setup_lines = []
        # _setup.py may need to import defs that its code references
        setup_refs = set()
        for node in post_import_nodes:
            for sub in ast.walk(node):
                if isinstance(sub, ast.Name) and sub.id in all_def_names:
                    setup_refs.add(sub.id)
        if setup_refs:
            # Group by their target module
            mod_to_names = {}
            for ref in setup_refs:
                rg = name_to_group.get(ref)
                if rg is not None:
                    other_group = groups[rg]
                    other_names = [od[1] for od in other_group if od[1] is not None]
                    other_pn = other_names[0] if len(other_names) == 1 else '_'.join(other_names[:3])
                    other_pn = ''.join(c for c in other_pn if c.isalnum() or c == '_').lower()[:60]
                    mod_to_names.setdefault(other_pn, []).append(ref)
            for mod, nms in sorted(mod_to_names.items()):
                setup_lines.append(f"from .{mod} import {', '.join(sorted(nms))}\n")
            setup_lines.append('\n')

        for node in post_import_nodes:
            setup_lines.append(''.join(lines[node.lineno-1:node.end_lineno]).rstrip() + '\n')
        (pkg_dir / '_setup.py').write_text(''.join(setup_lines), encoding='utf-8')

    # Write __init__.py
    init_lines = [''.join(''.join(lines[n.lineno-1:n.end_lineno]) for n in pre_import_nodes).rstrip() + '\n\n']
    for pn, nms in file_parts:
        for nm in nms:
            init_lines.append(f"from .{pn} import {nm}\n")
    if has_setup and post_import_names:
        init_lines.append(f"from ._setup import {', '.join(sorted(post_import_names))}\n")
    elif has_setup and post_import_nodes:
        # Side-effect-only setup: re-import to execute it
        init_lines.append("from . import _setup\n")

    (pkg_dir / '__init__.py').write_text(''.join(init_lines), encoding='utf-8')
    filepath.unlink()

    print(f" -> {len(groups)} files" + (" + _setup" if has_setup else ""))
    return True

def main():
    dirs = ['cb_agents','factory','factory/teams','distributed','router','visualizer','tests','run_guided_helpers']
    files = []
    for d in dirs:
        p = ROOT / d
        if p.exists():
            for f in sorted(p.glob("*.py")):
                files.append(f)
    for f in sorted(ROOT.glob("*.py")):
        if f.name.startswith('_') or f.name == 'simple_agent.py':
            continue
        files.append(f)

    count = 0
    for f in files:
        try:
            if refactor_file(f):
                count += 1
        except Exception as e:
            print(f"\n  ERROR on {f.name}: {e}")
            import traceback; traceback.print_exc()

    print(f"\nProcessed {count}/{len(files)} files.")

if __name__ == '__main__':
    main()
