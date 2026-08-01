
def split_large_class(source, lines, node):
    """Split a large class by extracting methods to helper functions."""
    name = node.name
    body = node.body
    
    methods = [n for n in body if isinstance(n, ast.FunctionDef)]
    other_items = [n for n in body if not isinstance(n, ast.FunctionDef)]
    
    # Find big methods
    big_methods = []
    small_methods = []
    for m in methods:
        m_len = m.end_lineno - m.lineno
        if m_len > 15:
            big_methods.append(m)
        else:
            small_methods.append(m)
    
    if not big_methods:
        return None
    
    # Build helpers
    helpers = []
    for m in big_methods:
        m_text = node_text(m, lines)
        helper_name = f"_{m.name}"
        # Convert method to function with self as first param
        # Get the method signature
        m_lines = m_text.splitlines(keepends=True)
        sig = m_lines[0].rstrip()
        # Replace def method_name(self, ...) with def _method_name(self, ...)
        sig = sig.replace(f'def {m.name}', f'def {helper_name}', 1)
        body_text = ''.join(m_lines[1:])
        h_func = sig + ':\n' + body_text
        helpers.append((helper_name, h_func))
        
        # Get args without self for the call
        args = [a.arg for a in m.args.args if a.arg != 'self']
        args += [a.arg for a in m.args.kwonlyargs]
        call_args = ', '.join(['self'] + args)
        
    # Build replacement class text
    class_line = node_text(node, lines).splitlines(keepends=True)[0].rstrip()
    repl = class_line + ':\n'
    indent = '    '
    
    for item in other_items:
        repl += indent + node_text(item, lines).rstrip() + '\n'
    
    for m in small_methods:
        repl += indent + node_text(m, lines).rstrip() + '\n'
    
    for m in big_methods:
        args = [a.arg for a in m.args.args if a.arg != 'self']
        args += [a.arg for a in m.args.kwonlyargs]
        call_args = ', '.join(['self'] + args)
        # Write stub method
        repl += indent + f'def {m.name}(self, {", ".join(args)}):\n'
        repl += indent * 2 + f'return _{m.name}({call_args})\n'
        repl += '\n'
    
    return repl, helpers

