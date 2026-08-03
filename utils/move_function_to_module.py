from pathlib import Path


def move_function_to_module(func_name: str, src_file: Path, dest_pkg: Path, dest_module_name: str) -> bool:
    # Extract function source lines
    with open(src_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    tree = ast.parse(''.join(lines), filename=str(src_file))
    func_node = None
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.FunctionDef) and node.name == func_name:
            func_node = node
            break
    if func_node is None:
        return False
    start = func_node.lineno - 1
    end = func_node.end_lineno
    func_code = ''.join(lines[start:end])
    # Write to destination module
    dest_pkg.mkdir(parents=True, exist_ok=True)
    dest_file = dest_pkg / f"{dest_module_name}.py"
    with open(dest_file, 'a', encoding='utf-8') as out:
        out.write('\n' + func_code + '\n')
    # Replace original definition with import statement
    import_line = f"from {dest_pkg.name}.{dest_module_name} import {func_name}\n"
    new_lines = lines[:start] + [import_line] + lines[end:]
    with open(src_file, 'w', encoding='utf-8') as out:
        out.writelines(new_lines)
    return True

