
def test___qualname___and___module___attribute():
    # NumPy messes with module and name/qualname attributes, but any object
    # should be discoverable based on its module and qualname, so test that.
    # We do this for anything with a name (ensuring qualname is also set).
    modules_queue = [np]
    visited_modules = {np}
    visited_functions = set()
    incorrect_entries = []

    while len(modules_queue) > 0:
        module = modules_queue.pop()
        for member_name in dir(module):
            member = getattr(module, member_name)
            # first check if we got a module
            if (
                inspect.ismodule(member) and  # it's a module
                "numpy" in member.__name__ and  # inside NumPy
                not member_name.startswith("_") and  # not private
                member_name not in {"tests", "typing"} and  # type names don't match
                "numpy._core" not in member.__name__ and  # outside _core
                member not in visited_modules  # not visited yet
            ):
                modules_queue.append(member)
                visited_modules.add(member)
            elif (
                not inspect.ismodule(member) and
                hasattr(member, "__name__") and
                not member.__name__.startswith("_") and
                not member_name.startswith("_") and
                not _check_correct_qualname_and_module(member) and
                member not in visited_functions
            ):
                incorrect_entries.append(
                    {
                        "found_at": f"{module.__name__}:{member_name}",
                        "advertises": f"{member.__module__}:{member.__qualname__}",
                    }
                )
                visited_functions.add(member)

    if incorrect_entries:
        assert len(incorrect_entries) == 0, incorrect_entries

