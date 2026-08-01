
def _get_overloaded_methods(method, mod_class):
    # TODO: __name__ not set for submodules in recursive script
    if not hasattr(method, "__name__"):
        return None
    qual_name = _qualified_name(method)
    class_name_map = _overloaded_methods.get(qual_name)
    if class_name_map is None:
        return None
    overloads = class_name_map.get(mod_class.__name__, None)
    if overloads is None:
        return None

    method_line_no = get_source_lines_and_file(method)[1]
    mod_class_fileno = get_source_lines_and_file(mod_class)[1]
    mod_end_fileno = mod_class_fileno + len(get_source_lines_and_file(mod_class)[0])
    if not (method_line_no >= mod_class_fileno and method_line_no <= mod_end_fileno):
        raise AssertionError(
            "Overloads are not usable when a module is redeclared within the same file: "
            + str(method)
        )
    return overloads

