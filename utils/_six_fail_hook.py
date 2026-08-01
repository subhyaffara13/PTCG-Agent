
def _six_fail_hook(modname):
    """Fix six.moves imports due to the dynamic nature of this
    class.

    Construct a pseudo-module which contains all the necessary imports
    for six

    :param modname: Name of failed module
    :type modname: str

    :return: An astroid module
    :rtype: nodes.Module
    """

    attribute_of = modname != "six.moves" and modname.startswith("six.moves")
    if modname != "six.moves" and not attribute_of:
        raise AstroidBuildingError(modname=modname)
    module = AstroidBuilder(AstroidManager()).string_build(_IMPORTS)
    module.name = "six.moves"
    if attribute_of:
        # Facilitate import of submodules in Moves
        start_index = len(module.name)
        attribute = modname[start_index:].lstrip(".").replace(".", "_")
        try:
            import_attr = module.getattr(attribute)[0]
        except AttributeInferenceError as exc:
            raise AstroidBuildingError(modname=modname) from exc
        if isinstance(import_attr, nodes.Import):
            submodule = AstroidManager().ast_from_module_name(import_attr.names[0][0])
            return submodule
    # Let dummy submodule imports pass through
    # This will cause an Uninferable result, which is okay
    return module

