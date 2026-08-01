
def is_module_ignored(
    qualified_module_name: str, ignored_modules: Iterable[str]
) -> bool:
    ignored_modules = set(ignored_modules)
    for current_module in _qualified_name_parts(qualified_module_name):
        # Try to match the module name directly
        if current_module in ignored_modules:
            return True
        for ignore in ignored_modules:
            # Try to see if the ignores pattern match against the module name.
            if fnmatch.fnmatch(current_module, ignore):
                return True
    return False

