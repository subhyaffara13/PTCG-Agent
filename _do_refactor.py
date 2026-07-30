"""Refactor all .py files >50 lines in target directories to be under 50 lines each."""
import ast
import shutil
import textwrap
import builtins
from pathlib import Path

ROOT = Path(r"C:\Users\subhy\.gemini\antigravity\scratch\ptcg-agent")
TARGET = 50
BUILTIN_NAMES = set(dir(builtins))

INCLUDE_DIRS = [
    "distributed",
    "router",
    "tests",
    "run_guided_helpers",
    "numpy_forward",
    "run_audit_pipeline",
]

# Sub-package dirs (already have __init__.py)
PACKAGE_DIRS = set()
for d in [
    "distributed/log_sync", "distributed/master_server",
    "distributed/master_handlers", "distributed/worker_client",
    "run_guided_helpers", "numpy_forward", "run_audit_pipeline",
    "tests/test_submission",
]:
    p = ROOT / d
    if p.exists() and (p / "__init__.py").exists():
        PACKAGE_DIRS.add(p.resolve())

def is_in_package(filepath):
    return filepath.parent.resolve() in PACKAGE_DIRS

# ---- AST helpers -----------------------------------------------------------

def _names_from_shared(node):
    if isinstance(node, ast.Import):
        for alias in node.names:
            yield alias.asname or alias.name.split('.')[0]
    elif isinstance(node, ast.ImportFrom):
        for alias in node.names:
            yield alias.asname or alias.name
    elif isinstance(node, ast.Assign):
        for t in node.targets:
            if isinstance(t, ast.Name):
                yield t.id
            elif isinstance(t, (ast.List, ast.Tuple)):
                for elt in t.elts:
                    if isinstance(elt, ast.Name):
                        yield elt.id
    elif isinstance(node, ast.AnnAssign):
        if isinstance(node.target, ast.Name):
            yield node.target.id
    elif isinstance(node, ast.Try):
        for c in node.body: yield from _names_from_shared(c)
        for h in node.handlers:
            for c in h.body: yield from _names_from_shared(c)
    elif isinstance(node, ast.If):
        for c in node.body: yield from _names_from_shared(c)

def _func_param_names(node):
    names = set()
    names.update(a.arg for a in node.args.args)
    names.update(a.arg for a in node.args.kwonlyargs)
    if node.args.vararg: names.add(node.args.vararg.arg)
    if node.args.kwarg: names.add(node.args.kwarg.arg)
    return names

def get_local_names(node):
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

def get_body_refs(source, func_names):
    tree = ast.parse(source)
    refs = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)) and node.name in func_names:
            local = get_local_names(node)
            for sub in ast.walk(node):
                if isinstance(sub, ast.Name) and sub.id not in BUILTIN_NAMES and sub.id not in local:
                    refs.add(sub.id)
    return refs

def _is_name_main(node):
    if not isinstance(node, ast.If): return False
    return (isinstance(node.test, ast.Compare)
            and isinstance(node.test.left, ast.Name) and node.test.left.id == '__name__'
            and len(node.test.ops) == 1 and isinstance(node.test.ops[0], ast.Eq)
            and len(node.test.comparators) == 1
            and isinstance(node.test.comparators[0], ast.Constant)
            and node.test.comparators[0].value == '__main__')

def node_text(node, lines):
    return ''.join(lines[node.lineno - 1:node.end_lineno])

def make_mod_name(names):
    """Create a module name from a list of def names."""
    if not names: return "part"
    base = names[0] if len(names) == 1 else '_'.join(names[:3])
    base = ''.join(c for c in base if c.isalnum() or c == '_').lower()[:60]
    if not base or base[0].isdigit(): base = "part"
    return base

# ---- Splitting a large def by extracting methods/sub-functions ------------

def split_large_def(lines, node, local_names_override=None):
    """
    Given a function/class def node that is > TARGET lines,
    extract its body-level statements into helper functions.
    Returns list of (helper_func_name, helper_text) pairs.
    """
    name = node.name
    start = node.lineno - 1
    end = node.end_lineno
    def_lines = lines[start:end]
    def_total = len(def_lines)
    
    # For a class: extract methods as standalone functions
    # For a function: extract top-level code blocks as sub-functions
    results = []
    
    if isinstance(node, ast.ClassDef):
        # Split class by extracting methods to _prefixed files
        # Each method becomes a standalone function that takes self as first param
        body_nodes = [n for n in node.body if isinstance(n, (ast.FunctionDef, ast.ClassDef, ast.Assign, ast.AnnAssign))]
        big_methods = [n for n in body_nodes if isinstance(n, ast.FunctionDef) and (n.end_lineno - n.lineno) > 15]
        
        if big_methods:
            # Extract big methods
            for m in big_methods:
                m_text = node_text(m, lines)
                func_name = m.name
                # Calculate the import needed
                m_refs = set()
                local = get_local_names(m)
                for sub in ast.walk(m):
                    if isinstance(sub, ast.Name) and sub.id not in BUILTIN_NAMES and sub.id not in local:
                        m_refs.add(sub.id)
                results.append((func_name, m_text, m_refs))
            
            # Create replacement class that delegates to the helpers
            # For each extracted method, add a stub method that calls the helper
            remaining_body = []
            for item in node.body:
                if isinstance(item, ast.FunctionDef) and any(r[0] == item.name for r in results):
                    # Create stub
                    item_lines = node_text(item, lines).splitlines(keepends=True)
                    sig = item_lines[0].rstrip()
                    stub = sig + ':\n'
                    # Get params except self
                    args = [a.arg for a in item.args.args if a.arg != 'self']
                    args += [a.arg for a in item.args.kwonlyargs]
                    if args:
                        call_args = ', '.join(args)
                        stub += f'    return _{item.name}(self, {call_args})\n'
                    else:
                        stub += f'    return _{item.name}(self)\n'
                    remaining_body.append(stub)
                else:
                    remaining_body.append(node_text(item, lines))
            
            # Build replacement class text
            head = node_text(node, lines).splitlines(keepends=True)[0]  # class X:
    indent = '    '
            repl = head.rstrip() + ':\n'
            for rb in remaining_body:
                for rb_line in rb.splitlines(keepends=True):
                    if rb_line.strip():
                        repl += indent + rb_line
                    else:
                        repl += '\n'
            results.append(('__replacement__', repl, set()))
    
    return results

# ---- Main refactoring function --------------------------------------------

def refactor_file(filepath):
    with open(filepath, encoding='utf-8') as f:
        source = f.read()
    lines = source.splitlines(keepends=True)
    total = len(lines)
    if total <= TARGET:
        return False

    name = filepath.name
    in_pkg = is_in_package(filepath)
    tag = "[pkg]" if in_pkg else "[std]"
    print(f"  {tag} {name} ({total} lines)...", end='')

    tree = ast.parse(source)

    shared_nodes = []
    def_nodes = []
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            def_nodes.append(node)
        else:
            shared_nodes.append(node)

    # Handle "no defs" case
    if not def_nodes:
        # Create a wrapper module - no splitting possible
        print(" -> no defs, cannot split")
        return False

    # Build def entries
    defs_with_text = []
    for node in def_nodes:
        text = node_text(node, lines)
        defs_with_text.append((node, node.name, node.lineno - 1, node.end_lineno, text))

    all_def_names = set(d[1] for d in defs_with_text)

    # Check if we have individual defs >50 lines that need intra-def splitting
    needs_intra_split = False
    intra_splits = {}  # def_name -> (replacement_text, [(helper_name, helper_text)])
    
    for node, dname, dstart, dend, dtext in defs_with_text:
        dlines = dend - dstart
        if dlines > TARGET:
            # This def itself is >50 lines - needs intra-def splitting
            splits = split_large_def(lines, node)
            if splits:
                needs_intra_split = True
                # Find the replacement entry
                repl_entry = None
                helpers = []
                for sname, stext, srefs in splits:
                    if sname == '__replacement__':
                        repl_entry = stext
                    else:
                        helpers.append((sname, stext, srefs))
                if repl_entry:
                    intra_splits[dname] = (repl_entry, helpers)
    
    # Separate shared nodes
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

    pre_import_names = set()
    for node in pre_import_nodes:
        for n in _names_from_shared(node): pre_import_names.add(n)
    post_import_names = set()
    for node in post_import_nodes:
        for n in _names_from_shared(node): post_import_names.add(n)

    # Group defs into sub-modules <= TARGET lines
    groups = []
    current, cur_size = [], 0
    
    for d in defs_with_text:
        node, dname, dstart, dend, dtext = d
        dlines = dend - dstart
        
        # If we have intra-def splits, use the replacement text which is smaller
        if dname in intra_splits:
            repl_text, helpers = intra_splits[dname]
            size = len(repl_text.splitlines())
        else:
            size = dlines
            
        if cur_size + size > TARGET and current:
            groups.append(current)
            current, cur_size = [], 0
        current.append(d)
        cur_size += size
    
    if current:
        groups.append(current)

    # If only 1 group exists but total file >50, we still split
    # Create at least 2 groups by moving some defs
    if len(groups) <= 1 and len(defs_with_text) >= 2:
        # Manual split: first half, second half
        mid = len(defs_with_text) // 2
        groups = [defs_with_text[:mid], defs_with_text[mid:]]
    elif len(groups) <= 1 and not intra_splits:
        # Single def >50 lines that couldn't be intra-split
        print(" -> large single def, can't split")
        return False

    # Rebuild name_to_group mapping
    name_to_group = {}
    for i, g in enumerate(groups):
        for d in g:
            name_to_group[d[1]] = i

    # Write sub-module files
    parent = filepath.parent
    
    if in_pkg:
        # Write as _prefixed files alongside the original
        for i, group in enumerate(groups):
            names = [d[1] for d in group if d[1] is not None]
            base = make_mod_name(names)
            
            # Determine imports for this module
            func_names_set = set()
            all_helpers = {}
            for d in group:
                dname = d[1]
                func_names_set.add(dname)
                if dname in intra_splits:
                    repl_text, helpers = intra_splits[dname]
                    for hn, ht, hr in helpers:
                        all_helpers[hn] = (ht, hr)
                        func_names_set.add(hn)
            
            refs = get_body_refs(source, func_names_set)
            
            shared_needed = set()
            cross_needed = {}
            for ref in refs:
                if ref in pre_import_names:
                    shared_needed.add(ref)
                elif ref in all_def_names:
                    rg = name_to_group.get(ref)
                    if rg is not None and rg != i:
                        other = groups[rg]
                        other_names = [od[1] for od in other if od[1] is not None]
                        other_base = make_mod_name(other_names)
                        cross_needed[ref] = other_base
            
            part_lines = []
            if shared_needed:
                part_lines.append(f"from . import {', '.join(sorted(shared_needed))}\n")
            if cross_needed:
                mod_to_names = {}
                for n, mod in cross_needed.items():
                    mod_to_names.setdefault(mod, []).append(n)
                for mod, nms in sorted(mod_to_names.items()):
                    part_lines.append(f"from ._{mod} import {', '.join(sorted(nms))}\n")
            if part_lines:
                part_lines.append('\n')
            
            for d in group:
                dname = d[1]
                if dname in intra_splits:
                    repl_text, helpers = intra_splits[dname]
                    part_lines.append(repl_text.rstrip() + '\n\n')
                    for hn, ht, hr in helpers:
                        part_lines.append(ht.rstrip() + '\n\n')
                else:
                    part_lines.append(d[4].rstrip() + '\n\n')
            
            (parent / f"_{base}.py").write_text(''.join(part_lines), encoding='utf-8')
        
        # Write _setup.py for post-import
        has_setup = bool(post_import_nodes)
        if has_setup:
            setup_lines = []
            setup_refs = set()
            for node in post_import_nodes:
                for sub in ast.walk(node):
                    if isinstance(sub, ast.Name) and sub.id in all_def_names:
                        setup_refs.add(sub.id)
            if setup_refs:
                mod_to_names = {}
                for ref in setup_refs:
                    rg = name_to_group.get(ref)
                    if rg is not None:
                        other = groups[rg]
                        other_names = [od[1] for od in other if od[1] is not None]
                        other_base = make_mod_name(other_names)
                        mod_to_names.setdefault(other_base, []).append(ref)
                for mod, nms in sorted(mod_to_names.items()):
                    setup_lines.append(f"from ._{mod} import {', '.join(sorted(nms))}\n")
                setup_lines.append('\n')
            for node in post_import_nodes:
                setup_lines.append(node_text(node, lines).rstrip() + '\n')
            (parent / '_setup.py').write_text(''.join(setup_lines), encoding='utf-8')
        
        # Rewrite original file as a slim shim
        shim = [''.join(node_text(n, lines) for n in pre_import_nodes).rstrip() + '\n\n']
        for i, group in enumerate(groups):
            names = [d[1] for d in group if d[1] is not None]
            base = make_mod_name(names)
            for d in group:
                dname = d[1]
                # Also import any helpers
                if dname in intra_splits:
                    repl_text, helpers = intra_splits[dname]
                    shim.append(f"from ._{base} import {dname}\n")
                    for hn, ht, hr in helpers:
                        shim.append(f"from ._{base} import {hn}\n")
                else:
                    shim.append(f"from ._{base} import {dname}\n")
        if has_setup and post_import_names:
            shim.append(f"from ._setup import {', '.join(sorted(post_import_names))}\n")
        elif has_setup:
            shim.append("from . import _setup\n")
        
        filepath.write_text(''.join(shim), encoding='utf-8')
    else:
        # Standalone file: convert to package directory
        shutil.copy2(filepath, str(filepath) + '.bak')
        pkg_dir = filepath.with_suffix('')
        pkg_dir.mkdir(exist_ok=True)
        
        file_parts = []
        for i, group in enumerate(groups):
            names = [d[1] for d in group if d[1] is not None]
            pn = make_mod_name(names)
            
            func_names_set = set()
            all_helpers = {}
            for d in group:
                dname = d[1]
                func_names_set.add(dname)
                if dname in intra_splits:
                    repl_text, helpers = intra_splits[dname]
                    for hn, ht, hr in helpers:
                        all_helpers[hn] = (ht, hr)
                        func_names_set.add(hn)
            
            refs = get_body_refs(source, func_names_set)
            
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
                        other = groups[rg]
                        other_names = [od[1] for od in other if od[1] is not None]
                        other_pn = make_mod_name(other_names)
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
                dname = d[1]
                if dname in intra_splits:
                    repl_text, helpers = intra_splits[dname]
                    part_lines.append(repl_text.rstrip() + '\n\n')
                    for hn, ht, hr in helpers:
                        part_lines.append(ht.rstrip() + '\n\n')
                else:
                    part_lines.append(d[4].rstrip() + '\n\n')
            
            (pkg_dir / f"{pn}.py").write_text(''.join(part_lines), encoding='utf-8')
            file_parts.append((pn, [d[1] for d in group if d[1] is not None]))
        
        has_setup = bool(post_import_nodes)
        if has_setup:
            setup_lines = []
            setup_refs = set()
            for node in post_import_nodes:
                for sub in ast.walk(node):
                    if isinstance(sub, ast.Name) and sub.id in all_def_names:
                        setup_refs.add(sub.id)
            if setup_refs:
                mod_to_names = {}
                for ref in setup_refs:
                    rg = name_to_group.get(ref)
                    if rg is not None:
                        other = groups[rg]
                        other_names = [od[1] for od in other if od[1] is not None]
                        other_pn = make_mod_name(other_names)
                        mod_to_names.setdefault(other_pn, []).append(ref)
                for mod, nms in sorted(mod_to_names.items()):
                    setup_lines.append(f"from .{mod} import {', '.join(sorted(nms))}\n")
                setup_lines.append('\n')
            for node in post_import_nodes:
                setup_lines.append(node_text(node, lines).rstrip() + '\n')
            (pkg_dir / '_setup.py').write_text(''.join(setup_lines), encoding='utf-8')
        
        init_lines = [''.join(node_text(n, lines) for n in pre_import_nodes).rstrip() + '\n\n']
        for pn, nms in file_parts:
            for nm in nms:
                init_lines.append(f"from .{pn} import {nm}\n")
        if has_setup and post_import_names:
            init_lines.append(f"from ._setup import {', '.join(sorted(post_import_names))}\n")
        elif has_setup:
            init_lines.append("from . import _setup\n")
        
        (pkg_dir / '__init__.py').write_text(''.join(init_lines), encoding='utf-8')
        filepath.unlink()

    print(f" -> {len(groups)} sub-modules")
    return True


def main():
    files = []
    for d in INCLUDE_DIRS:
        p = ROOT / d
        if p.exists():
            for f in sorted(p.rglob("*.py")):
                if f.name == "__init__.py": continue
                if f.name.startswith("_") and f.name != "__init__.py": continue
                files.append(f)

    count = 0
    for f in sorted(files):
        try:
            lines = len(f.read_text(encoding='utf-8').splitlines())
            if lines <= TARGET:
                continue
            if refactor_file(f):
                count += 1
        except Exception as e:
            print(f"\n  ERROR on {f.relative_to(ROOT)}: {e}")
            import traceback; traceback.print_exc()

    print(f"\nDone. {count} files refactored.")

if __name__ == "__main__":
    main()
