"""
Final refactoring script:
- Standalone .py files -> packages (dir with __init__.py + sub-modules)
- Sub-package files -> _prefixed helper extraction
- Large classes: extract methods into helpers
- Large functions: extract body into helpers
"""
import ast
import shutil
import re
from pathlib import Path

ROOT = Path(r"C:\Users\subhy\.gemini\antigravity\scratch\ptcg-agent")
TARGET = 50

# Which dirs to scan (all under these)
SCAN_DIRS = [
    "distributed", "router", "tests",
    "run_guided_helpers", "numpy_forward", "run_audit_pipeline",
]

# Directories that are already packages (their files get _prefixed extraction)
PKG_DIRS = set()
for candidate in [
    "run_guided_helpers", "numpy_forward", "run_audit_pipeline",
]:
    p = ROOT / candidate
    if p.exists() and (p / "__init__.py").exists():
        PKG_DIRS.add(p.resolve())


def is_pkg_file(fp):
    """Is this file inside a package dir (has __init__.py in parent)?"""
    return fp.parent.resolve() in PKG_DIRS


def node_text(node, lines):
    return ''.join(lines[node.lineno - 1:node.end_lineno])


def names_from_node(node):
    if isinstance(node, ast.Import):
        for a in node.names:
            yield a.asname or a.name.split('.')[0]
    elif isinstance(node, ast.ImportFrom):
        for a in node.names:
            yield a.asname or a.name
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
        for c in node.body:
            yield from names_from_node(c)
        for h in node.handlers:
            for c in h.body:
                yield from names_from_node(c)
    elif isinstance(node, ast.If):
        for c in node.body:
            yield from names_from_node(c)


def is_name_main(node):
    return (isinstance(node, ast.If)
            and isinstance(node.test, ast.Compare)
            and isinstance(node.test.left, ast.Name)
            and node.test.left.id == '__name__'
            and len(node.test.ops) == 1
            and isinstance(node.test.ops[0], ast.Eq)
            and len(node.test.comparators) == 1
            and isinstance(node.test.comparators[0], ast.Constant)
            and node.test.comparators[0].value == '__main__')


BUILTINS = set(dir(__builtins__))


def param_names(node):
    names = set()
    names.update(a.arg for a in node.args.args)
    names.update(a.arg for a in node.args.kwonlyargs)
    if node.args.vararg:
        names.add(node.args.vararg.arg)
    if node.args.kwarg:
        names.add(node.args.kwarg.arg)
    return names


def local_names(node):
    names = set()
    if isinstance(node, ast.FunctionDef):
        names |= param_names(node)
    if isinstance(node, ast.ClassDef):
        for item in node.body:
            if isinstance(item, ast.FunctionDef):
                names.add(item.name)
                names |= param_names(item)
            elif isinstance(item, ast.ClassDef):
                names.add(item.name)
    return names


def body_refs(source, func_names):
    tree = ast.parse(source)
    refs = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)) and node.name in func_names:
            local = local_names(node)
            for sub in ast.walk(node):
                if isinstance(sub, ast.Name) and sub.id not in BUILTINS and sub.id not in local:
                    refs.add(sub.id)
    return refs


def make_mod_name(names):
    if not names:
        return "part"
    base = names[0] if len(names) == 1 else '_'.join(names[:3])
    base = ''.join(c for c in base if c.isalnum() or c == '_').lower()[:60]
    if not base or base[0].isdigit():
        base = "part"
    return base


# ---------------------------------------------------------------------------
#  Refactor: Standalone file -> Package
# ---------------------------------------------------------------------------

def refactor_standalone(fp, source, lines, tree):
    """Convert a standalone .py into a package directory."""
    shared = []
    defs = []
    for n in ast.iter_child_nodes(tree):
        if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
            defs.append(n)
        else:
            shared.append(n)

    if not defs:
        return False

    def_entries = [(n, n.name, n.lineno - 1, n.end_lineno, node_text(n, lines)) for n in defs]
    all_names = set(d[1] for d in def_entries)

    # Separate shared
    pre = []
    post = []
    for n in shared:
        refs_def = any(isinstance(s, ast.Name) and s.id in all_names for s in ast.walk(n))
        (post if refs_def else pre).append(n)

    pre_names = set()
    for n in pre:
        for x in names_from_node(n):
            pre_names.add(x)
    post_names = set()
    for n in post:
        for x in names_from_node(n):
            post_names.add(x)

    # Group defs into chunks <= TARGET
    groups = []
    cur, cur_sz = [], 0
    for entry in def_entries:
        sz = entry[3] - entry[2]
        if cur_sz + sz > TARGET and cur:
            groups.append(cur)
            cur, cur_sz = [entry], sz
        else:
            cur.append(entry)
            cur_sz += sz
    if cur:
        groups.append(cur)

    # Always try to make at least 2 groups if file > TARGET
    if len(groups) <= 1 and len(def_entries) >= 2:
        mid = len(def_entries) // 2
        groups = [def_entries[:mid], def_entries[mid:]]

    if len(groups) <= 1:
        return False  # Single def too large, need class/function splitting

    name_to_group = {}
    for i, g in enumerate(groups):
        for d in g:
            name_to_group[d[1]] = i

    # Save .bak
    shutil.copy2(fp, str(fp) + '.bak')

    pkg = fp.with_suffix('')
    pkg.mkdir(exist_ok=True)

    parts_info = []
    for i, group in enumerate(groups):
        ns = [d[1] for d in group if d[1] is not None]
        mn = make_mod_name(ns)
        fns = set(d[1] for d in group if d[1] is not None)

        refs = body_refs(source, fns)

        shared_needed = set()
        cross_needed = {}
        setup_needed = set()
        for ref in refs:
            if ref in pre_names:
                shared_needed.add(ref)
            elif ref in post_names:
                setup_needed.add(ref)
            elif ref in all_names:
                rg = name_to_group.get(ref)
                if rg is not None and rg != i:
                    other = groups[rg]
                    other_ns = [od[1] for od in other if od[1] is not None]
                    other_mn = make_mod_name(other_ns)
                    cross_needed[ref] = other_mn

        chunk = []
        if shared_needed:
            chunk.append(f"from . import {', '.join(sorted(shared_needed))}\n")
        if setup_needed:
            chunk.append(f"from ._setup import {', '.join(sorted(setup_needed))}\n")
        if cross_needed:
            mod2n = {}
            for n, m in cross_needed.items():
                mod2n.setdefault(m, []).append(n)
            for m, nms in sorted(mod2n.items()):
                chunk.append(f"from .{m} import {', '.join(sorted(nms))}\n")
        if chunk:
            chunk.append('\n')

        for d in group:
            chunk.append(d[4].rstrip() + '\n\n')

        (pkg / f"{mn}.py").write_text(''.join(chunk), encoding='utf-8')
        parts_info.append((mn, [d[1] for d in group if d[1] is not None]))

    has_setup = bool(post)
    if has_setup:
        setup_lines = []
        setup_refs = set()
        for n in post:
            for s in ast.walk(n):
                if isinstance(s, ast.Name) and s.id in all_names:
                    setup_refs.add(s.id)
        if setup_refs:
            mod2n = {}
            for ref in setup_refs:
                rg = name_to_group.get(ref)
                if rg is not None:
                    other = groups[rg]
                    other_ns = [od[1] for od in other if od[1] is not None]
                    other_mn = make_mod_name(other_ns)
                    mod2n.setdefault(other_mn, []).append(ref)
            for m, nms in sorted(mod2n.items()):
                setup_lines.append(f"from .{m} import {', '.join(sorted(nms))}\n")
            setup_lines.append('\n')
        for n in post:
            setup_lines.append(node_text(n, lines).rstrip() + '\n')
        (pkg / '_setup.py').write_text(''.join(setup_lines), encoding='utf-8')

    init = [''.join(node_text(n, lines) for n in pre).rstrip() + '\n\n']
    for mn, nms in parts_info:
        for nm in nms:
            init.append(f"from .{mn} import {nm}\n")
    if has_setup and post_names:
        init.append(f"from ._setup import {', '.join(sorted(post_names))}\n")
    elif has_setup:
        init.append("from . import _setup\n")

    (pkg / '__init__.py').write_text(''.join(init), encoding='utf-8')
    fp.unlink()
    return True


# ---------------------------------------------------------------------------
#  Refactor: File in sub-package -> _prefixed helpers
# ---------------------------------------------------------------------------

def split_large_def(fp, source, lines, tree):
    """
    For a file with a single large function/class (>50 lines):
        Extract body parts into _helper files.
    """
    defs = [n for n in ast.iter_child_nodes(tree) if isinstance(n, (ast.FunctionDef, ast.ClassDef))]

    if not defs:
        return False

    big = [n for n in defs if (n.end_lineno - n.lineno) > TARGET]
    if not big:
        return False

    node = big[0]
    shared = [n for n in ast.iter_child_nodes(tree) if not isinstance(n, (ast.FunctionDef, ast.ClassDef))]

    if isinstance(node, ast.ClassDef):
        return _split_class(fp, source, lines, node, shared)
    elif isinstance(node, ast.FunctionDef):
        return _split_function(fp, source, lines, node, shared)

    return False


def _split_class(fp, source, lines, cls_node, shared_nodes):
    """Split a large class by extracting methods into a _helpers file."""
    methods = [n for n in cls_node.body if isinstance(n, ast.FunctionDef)]
    big = [m for m in methods if (m.end_lineno - m.lineno) > 15]

    if not big:
        return False

    cls_name = cls_node.name
    parent = fp.parent
    base_name = fp.stem.replace('_', '', 1) if fp.stem.startswith('_') else fp.stem
    helper_mod = f"_{base_name}_helpers"

    # Extract big methods as helpers
    helpers = []
    for m in big:
        h_name = f"_{m.name}"
        m_text = node_text(m, lines)

        # Convert method to function
        m_lines = m_text.splitlines(keepends=True)
        sig = m_lines[0].rstrip()
        sig = re.sub(r'^(\s*)def\s+' + re.escape(m.name), r'\1def ' + h_name, sig)

        body = ''.join(m_lines[1:])
        h_text = sig + '\n' + body
        helpers.append((h_name, m.name, h_text))

    # Write _helpers file
    h_texts = []
    h_names = []
    for hn, mn, ht in helpers:
        h_texts.append(ht + '\n\n')
        h_names.append(hn)
    (parent / f"{helper_mod}.py").write_text(''.join(h_texts), encoding='utf-8')

    # Rebuild class: keep small methods, add stubs for big ones
    cls_line = node_text(cls_node, lines).splitlines(keepends=True)[0].rstrip()
    new_cls = [cls_line + '\n']
    indent = '    '

    non_methods = [n for n in cls_node.body if not isinstance(n, ast.FunctionDef)]
    small = [m for m in methods if m not in big]

    for item in non_methods:
        new_cls.append(indent + node_text(item, lines).rstrip() + '\n')

    for m in small:
        new_cls.append(node_text(m, lines).rstrip() + '\n')

    for hn, mn, ht in helpers:
        # Build stub
        args = [a.arg for a in next(m for m in big if m.name == mn).args.args if a.arg != 'self']
        args.extend(a.arg for a in next(m for m in big if m.name == mn).args.kwonlyargs)
        call = ', '.join(['self'] + args)
        stub = f"{indent}def {mn}(self, {', '.join(args)}):\n"
        stub += f"{indent * 2}return {hn}({call})\n"
        new_cls.append(stub + '\n')

    # Combine with pre-class imports
    pre_text = ''.join(node_text(n, lines) for n in shared_nodes).rstrip()
    new_content = pre_text + '\n\n'
    if h_names:
        new_content += f"from .{helper_mod} import {', '.join(h_names)}\n"
    new_content += '\n'
    new_content += ''.join(new_cls)

    fp.write_text(new_content, encoding='utf-8')
    return True


def _split_function(fp, source, lines, fn_node, shared_nodes):
    """Split a large function by extracting try/if/for blocks into helpers."""
    body = fn_node.body
    # Find block-level statements that are large
    blocks = [s for s in body if isinstance(s, (ast.Try, ast.If, ast.For, ast.While)) and (s.end_lineno - s.lineno) > 20]

    if not blocks:
        return False

    parent = fp.parent
    base_name = fp.stem.replace('_', '', 1) if fp.stem.startswith('_') else fp.stem
    helper_mod = f"_{base_name}_helpers"
    fn_name = fn_node.name

    # Extract each block as a helper
    helpers = []
    for i, blk in enumerate(blocks):
        h_name = f"_{fn_name}_{i}"
        blk_text = node_text(blk, lines)

        # Dedent by 4
        blk_lines = blk_text.splitlines(keepends=True)
        dedented = []
        for bl in blk_lines:
            if bl.startswith('    '):
                dedented.append(bl[4:])
            else:
                dedented.append(bl)
        h_text = f"def {h_name}({', '.join([''])}):\n" + ''.join(dedented)
        helpers.append((h_name, h_text))

    # Write helpers file
    h_texts = []
    h_names = []
    for hn, ht in helpers:
        h_texts.append(ht + '\n\n')
        h_names.append(hn)
    (parent / f"{helper_mod}.py").write_text(''.join(h_texts), encoding='utf-8')

    # Build replacement function
    fn_head = node_text(fn_node, lines).splitlines(keepends=True)[0].rstrip()
    new_fn = [fn_head + '\n']
    indent = '    '

    other_stmts = [s for s in body if s not in blocks]
    for stmt in other_stmts:
        new_fn.append(indent + node_text(stmt, lines).rstrip() + '\n')

    for i, (hn, ht) in enumerate(helpers):
        new_fn.append(f"{indent}{hn}()\n")

    pre_text = ''.join(node_text(n, lines) for n in shared_nodes).rstrip()
    new_content = pre_text + '\n\n'
    if h_names:
        new_content += f"from .{helper_mod} import {', '.join(h_names)}\n"
    new_content += '\n'
    new_content += ''.join(new_fn)

    fp.write_text(new_content, encoding='utf-8')
    return True


# ---------------------------------------------------------------------------
#  Refactor: file in sub-package -> _prefixed module extraction
# ---------------------------------------------------------------------------

def refactor_pkg_file(fp, source, lines, tree):
    """Split a file in a sub-package by extracting defs into _prefixed files."""
    shared = []
    defs = []
    for n in ast.iter_child_nodes(tree):
        if isinstance(n, (ast.FunctionDef, ast.ClassDef)):
            defs.append(n)
        else:
            shared.append(n)

    if not defs:
        return False

    def_entries = [(n, n.name, n.lineno - 1, n.end_lineno, node_text(n, lines)) for n in defs]
    all_names = set(d[1] for d in def_entries)

    # Separate pre/post shared
    pre = []
    post = []
    for n in shared:
        refs_def = any(isinstance(s, ast.Name) and s.id in all_names for s in ast.walk(n))
        (post if refs_def else pre).append(n)

    pre_names = set()
    for n in pre:
        for x in names_from_node(n):
            pre_names.add(x)
    post_names = set()
    for n in post:
        for x in names_from_node(n):
            post_names.add(x)

    # Group defs
    groups = []
    cur, cur_sz = [], 0
    for entry in def_entries:
        sz = entry[3] - entry[2]
        if cur_sz + sz > TARGET and cur:
            groups.append(cur)
            cur, cur_sz = [entry], sz
        else:
            cur.append(entry)
            cur_sz += sz
    if cur:
        groups.append(cur)

    if len(groups) <= 1 and len(def_entries) >= 2:
        mid = len(def_entries) // 2
        groups = [def_entries[:mid], def_entries[mid:]]

    if len(groups) <= 1:
        return False  # Single large def

    name_to_group = {}
    for i, g in enumerate(groups):
        for d in g:
            name_to_group[d[1]] = i

    parent = fp.parent

    for i, group in enumerate(groups):
        ns = [d[1] for d in group if d[1] is not None]
        mn = make_mod_name(ns)
        fns = set(d[1] for d in group if d[1] is not None)

        refs = body_refs(source, fns)

        shared_needed = set()
        cross_needed = {}
        for ref in refs:
            if ref in pre_names:
                shared_needed.add(ref)
            elif ref in all_names:
                rg = name_to_group.get(ref)
                if rg is not None and rg != i:
                    other = groups[rg]
                    other_ns = [od[1] for od in other if od[1] is not None]
                    other_mn = make_mod_name(other_ns)
                    cross_needed[ref] = other_mn

        chunk = []
        if shared_needed:
            chunk.append(f"from . import {', '.join(sorted(shared_needed))}\n")
        if cross_needed:
            mod2n = {}
            for n, m in cross_needed.items():
                mod2n.setdefault(m, []).append(n)
            for m, nms in sorted(mod2n.items()):
                chunk.append(f"from ._{m} import {', '.join(sorted(nms))}\n")
        if chunk:
            chunk.append('\n')

        for d in group:
            chunk.append(d[4].rstrip() + '\n\n')

        (parent / f"_{mn}.py").write_text(''.join(chunk), encoding='utf-8')

    # Rewrite original as shim
    shim = [''.join(node_text(n, lines) for n in pre).rstrip() + '\n\n']
    for i, group in enumerate(groups):
        ns = [d[1] for d in group if d[1] is not None]
        mn = make_mod_name(ns)
        for d in group:
            shim.append(f"from ._{mn} import {d[1]}\n")
    if post:
        if post_names:
            shim.append(f"from ._setup import {', '.join(sorted(post_names))}\n")
        else:
            shim.append("from . import _setup\n")
        # Write _setup.py
        setup_lines = []
        setup_refs = set()
        for n in post:
            for s in ast.walk(n):
                if isinstance(s, ast.Name) and s.id in all_names:
                    setup_refs.add(s.id)
        if setup_refs:
            mod2n = {}
            for ref in setup_refs:
                rg = name_to_group.get(ref)
                if rg is not None:
                    other = groups[rg]
                    other_ns = [od[1] for od in other if od[1] is not None]
                    other_mn = make_mod_name(other_ns)
                    mod2n.setdefault(other_mn, []).append(ref)
            for m, nms in sorted(mod2n.items()):
                setup_lines.append(f"from ._{m} import {', '.join(sorted(nms))}\n")
            setup_lines.append('\n')
        for n in post:
            setup_lines.append(node_text(n, lines).rstrip() + '\n')
        (parent / '_setup.py').write_text(''.join(setup_lines), encoding='utf-8')

    fp.write_text(''.join(shim), encoding='utf-8')
    return True


# ---------------------------------------------------------------------------
#  Main
# ---------------------------------------------------------------------------

def main():
    files = []
    for d in SCAN_DIRS:
        p = ROOT / d
        if p.exists():
            for f in sorted(p.rglob("*.py")):
                rel = f.relative_to(ROOT)
                # Skip __init__.py, _setup.py, _helpers files
                if f.name == "__init__.py":
                    continue
                if f.name == "_setup.py":
                    continue
                if f.stem.endswith("_helpers"):
                    continue
                files.append(f)

    count = 0
    for fp in sorted(files):
        try:
            text = fp.read_text(encoding='utf-8')
            lines = text.splitlines()
            if len(lines) <= TARGET:
                continue

            rel = fp.relative_to(ROOT)
            print(f"  {rel} ({len(lines)} lines)...", end='')

            tree = ast.parse(text)
            ok = False

            if is_pkg_file(fp):
                # Try extracting defs to _prefixed files
                ok = refactor_pkg_file(fp, text, lines, tree)
                if not ok:
                    # Try splitting large single def
                    ok = split_large_def(fp, text, lines, tree)
            else:
                # Convert standalone to package
                ok = refactor_standalone(fp, text, lines, tree)
                if not ok:
                    ok = split_large_def(fp, text, lines, tree)

            if ok:
                print(" OK")
                count += 1
            else:
                print(" SKIP (can't split)")
        except SyntaxError:
            print(f"  {fp.relative_to(ROOT)}: syntax error")
        except Exception as e:
            print(f"  {fp.relative_to(ROOT)}: ERROR {e}")
            import traceback
            traceback.print_exc()

    print(f"\nRefactored: {count} files")


if __name__ == '__main__':
    main()
