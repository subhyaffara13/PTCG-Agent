
def _generic_io_transform(node, name, cls):
    """Transform the given name, by adding the given *class* as a member of the
    node.
    """

    io_module = AstroidManager().ast_from_module_name("_io")
    attribute_object = io_module[cls]
    instance = attribute_object.instantiate_class()
    node.locals[name] = [instance]

