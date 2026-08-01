
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

