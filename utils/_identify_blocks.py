
def _identify_blocks(func_node, lines):
    """Identify logical blocks within a function based on top-level if/elif chains and comments."""
    blocks = []
    
    if not func_node.body:
        return blocks
    
    # Look for comment-delineated blocks
    current_start = None
    current_label = ""
    in_chain = False
    
    for item in func_node.body:
        lineno = item.lineno
        
        # Check for comment on previous line
        comment_line = lines[lineno-2] if lineno > 1 else ""
        has_comment = comment_line.strip().startswith('#')
        
        if has_comment:
            if current_start is not None:
                blocks.append((current_start, lineno-1, current_label))
            current_start = lineno
            current_label = comment_line.strip('# ')
        elif isinstance(item, ast.If) and not in_chain:
            in_chain = True
            if current_start is not None:
                blocks.append((current_start, lineno-1, current_label))
            current_start = lineno
            current_label = f"if_{item.test}"
        elif isinstance(item, (ast.Assign, ast.Expr, ast.AugAssign)):
            if current_start is None:
                current_start = lineno
                current_label = "setup"
    
    if current_start is not None:
        blocks.append((current_start, func_node.end_lineno, current_label))
    
    return blocks

