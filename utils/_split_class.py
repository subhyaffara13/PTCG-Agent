
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

