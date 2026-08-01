
def _refactor_class(class_node, lines, pkg_dir, shared_text):
    """Extract methods from a large class into separate helper files."""
    methods = []
    others = []
    for item in class_node.body:
        if isinstance(item, ast.FunctionDef):
            methods.append(item)
        else:
            others.append(item)
    
    helpers = []
    for method in methods:
        mlen = method.end_lineno - method.lineno + 1
        if mlen <= LINE_LIMIT:
            continue
        
        # Extract this method into a separate file
        mtext = ''.join(lines[method.lineno-1:method.end_lineno])
        hname = f"_{method.name}"
        hfile_name = f"_{class_node.name}_{method.name}.py"
        
        # Create helper file
        hfile_path = pkg_dir / hfile_name
        hfile_path.write_text(
            f"from . import *\n\n"
            f"def {hname}(self, *args, **kwargs):\n"
            f"    {mtext.replace(chr(10), chr(10)+'    ')}\n",
            encoding='utf-8'
        )
        
        helpers.append((hname, hfile_name.replace('.py', '')))
    
    # Create new class with trimmed methods
    new_body = []
    for item in class_node.body:
        if isinstance(item, ast.FunctionDef):
            mlen = item.end_lineno - item.lineno + 1
            if mlen <= LINE_LIMIT:
                new_body.append(item)
            else:
                # Replace with stub
                stub = ast.FunctionDef(
                    name=item.name,
                    args=item.args,
                    body=[ast.Expr(value=ast.Constant(value=Ellipsis))],
                    decorator_list=item.decorator_list,
                    lineno=item.lineno,
                    col_offset=item.col_offset,
                    end_lineno=item.lineno,
                    end_col_offset=item.col_offset,
                    returns=item.returns,
                )
                new_body.append(stub)
        else:
            new_body.append(item)
    
    class_node.body = new_body
    return (class_node, helpers)

