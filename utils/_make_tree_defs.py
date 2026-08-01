
def _make_tree_defs(mod_files_list: ItemsView[str, set[str]]) -> _ImportTree:
    """Get a list of 2-uple (module, list_of_files_which_import_this_module),
    it will return a dictionary to represent this as a tree.
    """
    tree_defs: _ImportTree = {}
    for mod, files in mod_files_list:
        node: list[_ImportTree | list[str]] = [tree_defs, []]
        for prefix in mod.split("."):
            assert isinstance(node[0], dict)
            node = node[0].setdefault(prefix, ({}, []))  # type: ignore[arg-type,assignment]
        assert isinstance(node[1], list)
        node[1].extend(files)
    return tree_defs

