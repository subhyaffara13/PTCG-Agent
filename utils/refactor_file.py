
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


def refactor_file(filepath):
    """Handle a single file with a large def."""
    with open(filepath, encoding='utf-8') as f:
        source = f.read()
    lines = source.splitlines(keepends=True)
    total = len(lines)
    if total <= TARGET:
        return False
    
    print(f"  {filepath.relative_to(ROOT)} ({total} lines)...", end='')
    
    tree = ast.parse(source)
    
    def_nodes = [n for n in ast.iter_child_nodes(tree) if isinstance(n, (ast.FunctionDef, ast.ClassDef))]
    
    if not def_nodes:
        print(" no defs")
        return False
    
    # Check if any single def is >50 lines
    large_defs = []
    for n in def_nodes:
        dsize = n.end_lineno - n.lineno
        if dsize > TARGET:
            large_defs.append(n)
    
    if not large_defs:
        # No def is individually large, but file is >50 lines
        # Try splitting at def level
        print(" multi-def, handle via grouping")
        return False
    
    # We have a single def >50 lines - try to split it
    node = large_defs[0]
    parent = filepath.parent
    is_prefixed = filepath.name.startswith('_')
    
    result = None
    if isinstance(node, ast.FunctionDef):
        result = split_large_function(source, lines, node)
    elif isinstance(node, ast.ClassDef):
        result = split_large_class(source, lines, node)
    
    if result is None:
        print(" can't split")
        return False
    
    repl_text, helpers = result
    
    # Write the helper to a _prefixed file
    base_name = filepath.stem.replace('_', '', 1) if is_prefixed else filepath.stem
    helper_mod = f"_{base_name}_helpers"
    
    helper_lines = []
    m_names = []
    for hn, ht in helpers:
        # Figure out what imports this helper needs
        helper_lines.append(ht + '\n\n')
        m_names.append(hn)
    
    (parent / f"{helper_mod}.py").write_text(''.join(helper_lines), encoding='utf-8')
    
    # Rewrite the original file
    # Get the pre-import nodes
    shared_nodes = [n for n in ast.iter_child_nodes(tree) if not isinstance(n, (ast.FunctionDef, ast.ClassDef))]
    pre_import = ''.join(node_text(n, lines) for n in shared_nodes).rstrip()
    
    if is_prefixed:
        # The file is already a _prefixed sub-module of a package shim
        # We need to rewrite it with import + replacement + helpers
        # But also update the shim that imports from this file
        new_content = pre_import + '\n\n'
        if m_names:
            new_content += f"from .{helper_mod} import {', '.join(m_names)}\n"
        new_content += '\n'
        new_content += repl_text
        filepath.write_text(new_content, encoding='utf-8')
    else:
        # Standalone file or package file
        new_content = pre_import + '\n\n'
        if m_names:
            # Import from the helper module (relative or absolute)
            new_content += f"from .{helper_mod} import {', '.join(m_names)}\n"
        new_content += '\n'
        new_content += repl_text
        # Save .bak
        bak_path = str(filepath) + '.bak'
        if not filepath.with_suffix('.py.bak').exists():
            shutil.copy2(filepath, bak_path)
        filepath.write_text(new_content, encoding='utf-8')
    
    print(f" -> extracted {len(helpers)} helpers to {helper_mod}.py")
    return True


def refactor_file(filepath):
    """Refactor a single large file by extracting helpers."""
    filepath = Path(filepath)
    source = filepath.read_text(encoding='utf-8')
    lines = source.splitlines(keepends=True)
    total = len(lines)
    if total <= LINE_LIMIT:
        return None

    name = filepath.name
    stem = filepath.stem
    pkg_dir = filepath.parent
    pkg_init = pkg_dir / '__init__.py'

    print(f"\n{'='*60}")
    print(f"Refactoring: {filepath.relative_to(ROOT)} ({total} lines)")

    tree = ast.parse(source)
    
    # Identify top-level defs
    top_defs = []
    shared_lines = []
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            top_defs.append(node)
        else:
            shared_lines.append((node.lineno, node.end_lineno))

    # Get shared (imports/constants) source
    shared_source_lines = []
    for lo, hi in shared_lines:
        shared_source_lines.extend(lines[lo-1:hi])
    shared_text = ''.join(shared_source_lines)

    new_defs = {}
    
    for node in top_defs:
        nd_lines = node.end_lineno - node.lineno + 1
        nlen = len(node.name)
        
        if nd_lines <= LINE_LIMIT:
            new_defs[node.name] = (node, None)
            continue

        if isinstance(node, ast.ClassDef):
            result = _refactor_class(node, lines, pkg_dir, shared_text)
        elif isinstance(node, ast.FunctionDef):
            result = _refactor_function(node, lines, pkg_dir, shared_text)
        else:
            new_defs[node.name] = (node, None)
            continue

        if result:
            new_defs[node.name] = result

    # Write the main file
    main_defs = []
    imports_needed = {}
    
    for name, (def_node, helpers) in new_defs.items():
        if helpers:
            for hname, hfile in helpers:
                imports_needed.setdefault(hfile, []).append(hname)
        main_defs.append(def_node)
    
    # Build new main file content
    new_lines = []
    # Shared code
    if shared_text.strip():
        new_lines.append(shared_text.rstrip() + '\n\n')
    
    # Import helpers
    for hfile, hnames in sorted(imports_needed.items()):
        new_lines.append(f"from .{hfile} import {', '.join(sorted(hnames))}\n")
    if imports_needed:
        new_lines.append('\n')
    
    # Keep only trimmed defs
    for def_node in main_defs:
        # Read the original text
        dtext = ''.join(lines[def_node.lineno-1:def_node.end_lineno])
        new_lines.append(dtext.rstrip() + '\n\n')
    
    # Trim original file
    new_content = ''.join(new_lines)
    new_lines_count = len(new_content.splitlines())
    
    print(f"  -> {stem}.py trimmed to {new_lines_count} lines")
    
    # Create backup
    bak_path = str(filepath) + '.bak'
    if not Path(bak_path).exists():
        shutil.copy2(filepath, bak_path)
    
    filepath.write_text(new_content, encoding='utf-8')
    
    # Update __init__.py if needed — ensure all top-level names are re-exported
    _ensure_exports_in_init(filepath, top_defs, pkg_init)
    
    return new_defs

