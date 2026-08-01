
def KDTreeTest(kls):
    """Class decorator to create test cases for KDTree and cKDTree

    Tests use the class variable ``kdtree_type`` as the tree constructor.
    """
    if not kls.__name__.startswith('_Test'):
        raise RuntimeError("Expected a class name starting with _Test")

    for tree in (KDTree, cKDTree):
        test_name = kls.__name__[1:] + '_' + tree.__name__

        if test_name in globals():
            raise RuntimeError("Duplicated test name: " + test_name)

        # Create a new sub-class with kdtree_type defined
        test_case = type(test_name, (kls,), {'kdtree_type': tree})
        globals()[test_name] = test_case
    return kls

