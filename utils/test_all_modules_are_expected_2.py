
def test_all_modules_are_expected_2():
    """
    Method checking all objects. The pkgutil-based method in
    `test_all_modules_are_expected` does not catch imports into a namespace,
    only filenames.
    """

    def find_unexpected_members(mod_name):
        members = []
        module = importlib.import_module(mod_name)
        if hasattr(module, '__all__'):
            objnames = module.__all__
        else:
            objnames = dir(module)

        for objname in objnames:
            if not objname.startswith('_'):
                fullobjname = mod_name + '.' + objname
                if isinstance(getattr(module, objname), types.ModuleType):
                    if is_unexpected(fullobjname) and fullobjname not in SKIP_LIST_2:
                        members.append(fullobjname)

        return members
    with warnings.catch_warnings():
        warnings.filterwarnings("ignore",  "scipy.misc", DeprecationWarning)
        unexpected_members = find_unexpected_members("scipy")

    for modname in PUBLIC_MODULES:
        unexpected_members.extend(find_unexpected_members(modname))

    if unexpected_members:
        raise AssertionError("Found unexpected object(s) that look like "
                             f"modules: {unexpected_members}")


def test_all_modules_are_expected_2():
    """
    Method checking all objects. The pkgutil-based method in
    `test_all_modules_are_expected` does not catch imports into a namespace,
    only filenames.  So this test is more thorough, and checks this like:

        import .lib.scimath as emath

    To check if something in a module is (effectively) public, one can check if
    there's anything in that namespace that's a public function/object but is
    not exposed in a higher-level namespace.  For example for a `numpy.lib`
    submodule::

        mod = np.lib.mixins
        for obj in mod.__all__:
            if obj in np.__all__:
                continue
            elif obj in np.lib.__all__:
                continue

            else:
                print(obj)

    """

    def find_unexpected_members(mod_name):
        members = []
        module = importlib.import_module(mod_name)
        if hasattr(module, '__all__'):
            objnames = module.__all__
        else:
            objnames = dir(module)

        for objname in objnames:
            if not objname.startswith('_'):
                fullobjname = mod_name + '.' + objname
                if isinstance(getattr(module, objname), types.ModuleType):
                    if is_unexpected(fullobjname):
                        if fullobjname not in SKIP_LIST_2:
                            members.append(fullobjname)

        return members

    unexpected_members = find_unexpected_members("numpy")
    for modname in PUBLIC_MODULES:
        unexpected_members.extend(find_unexpected_members(modname))

    if unexpected_members:
        raise AssertionError("Found unexpected object(s) that look like "
                             f"modules: {unexpected_members}")

