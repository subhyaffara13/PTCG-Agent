
def _refactor_function(func_node, lines, pkg_dir, shared_text):
    """Extract logical blocks from a large function into separate helper files."""
    func_text = ''.join(lines[func_node.lineno-1:func_node.end_lineno])
    func_lines_count = func_node.end_lineno - func_node.lineno + 1
    
    if func_lines_count <= LINE_LIMIT:
        return (func_node, None)
    
    # For functions, extract based on comment blocks or if/elif chains
    blocks = _identify_blocks(func_node, lines)
    
    if not blocks or len(blocks) < 2:
        return (func_node, None)
    
    helpers = []
    
    for i, (start, end, label) in enumerate(blocks):
        if start is None:
            continue
        block_text = ''.join(lines[start-1:end])
        safe_label = ''.join(c if c.isalnum() else '_' for c in label)[:40].strip('_').lower()
        if not safe_label:
            safe_label = f"block_{i}"
        if safe_label[0].isdigit():
            safe_label = f"b{safe_label}"
        
        hname = f"_{func_node.name}_{safe_label}"
        hfile_name = f"_{func_node.name}_{safe_label}.py"
        
        hfile_path = pkg_dir / hfile_name
        hfile_path.write_text(block_text, encoding='utf-8')
        
        helpers.append((hname, hfile_name.replace('.py', '')))
    
    if helpers:
        # Replace function body with calls to helpers
        stub_body = []
        for hname, _ in helpers:
            stub_body.append(
                ast.Expr(value=ast.Call(
                    func=ast.Name(id=hname, ctx=ast.Load()),
                    args=[],
                    keywords=[]
                ))
            )
        func_node.body = stub_body
        return (func_node, helpers)
    
    return (func_node, None)

