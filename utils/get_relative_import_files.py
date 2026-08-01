
def get_relative_import_files(module_file: str | os.PathLike) -> list[str]:
    """
    Get the list of all files that are needed for a given module. Note that this function recurses through the relative
    imports (if a imports b and b imports c, it will return module files for b and c).

    Args:
        module_file (`str` or `os.PathLike`): The module file to inspect.

    Returns:
        `list[str]`: The list of all relative imports a given module needs (recursively), which will give us the list
        of module files a given module needs.
    """
    no_change = False
    files_to_check = [module_file]
    all_relative_imports = []

    # Let's recurse through all relative imports
    while not no_change:
        new_imports = []
        for f in files_to_check:
            new_imports.extend(get_relative_imports(f))

        module_path = Path(module_file).parent
        new_import_files = [f"{str(module_path / m)}.py" for m in new_imports]
        files_to_check = [f for f in new_import_files if f not in all_relative_imports]

        no_change = len(files_to_check) == 0
        all_relative_imports.extend(files_to_check)

    return all_relative_imports

