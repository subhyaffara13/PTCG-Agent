
def split_large_function(source, lines, node):
    """Split a large function (>50 lines) by extracting block-level sections."""
    name = node.name
    f_start = node.lineno - 1
    f_end = node.end_lineno
    
    # Get the function's body (statements at top level of function)
    body = node.body
    
    # Find major blocks that can be extracted
    # Look for try/except, if/elif/else, for, while blocks at top level
    blocks = []
    other_stmts = []
    
    for stmt in body:
        line_len = stmt.end_lineno - stmt.lineno
        if line_len > 20:
            blocks.append(stmt)
        else:
            other_stmts.append(stmt)
    
    if not blocks:
        return None  # Can't split
    
    # Extract each block as a helper function
    helpers = []
    for i, block in enumerate(blocks):
        helper_name = f"_{name}_{i}"
        helper_text = node_text(block, lines)
        # Build the helper function
        h_func = f"def {helper_name}():\n"
        for line in helper_text.splitlines(keepends=True):
            h_func += '    ' + line
        helpers.append((helper_name, h_func.rstrip() + '\n'))
    
    # Build replacement function with calls to helpers
    repl_func = node_text(node, lines).splitlines(keepends=True)[0].rstrip() + ':\n'
    indent = '    '
    
    # Add other stmts first
    for stmt in other_stmts:
        repl_func += indent + node_text(stmt, lines).rstrip()
    
    # Add calls to helpers where the blocks were
    for i, (hn, ht) in enumerate(helpers):
        repl_func += indent + f'{hn}()\n'
    
    return repl_func, helpers

