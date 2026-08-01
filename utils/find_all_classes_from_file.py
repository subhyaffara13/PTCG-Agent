
def find_all_classes_from_file(module_name: str) -> set:
    """
    Find the name of all classes defined in `module_name`, including public ones (defined in `__all__`).

    Args:
        module_name (`str`):
            The full path to the python module from which to extract classes.
    """
    with open(module_name, "r", encoding="utf-8") as file:
        source_code = file.read()
    module = cst.parse_module(source_code)
    visitor = ClassFinder()
    module.visit(visitor)
    return visitor.classes, visitor.public_classes

