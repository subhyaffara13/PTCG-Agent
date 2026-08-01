
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

