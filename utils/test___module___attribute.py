
def test___module___attribute():
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
                "numpy._core" not in member.__name__ and  # outside _core
                # not in a skip module list
                member_name not in [
                    "char", "core", "f2py", "ma", "lapack_lite", "mrecords",
                    "testing", "tests", "polynomial", "typing", "mtrand",
                    "bit_generator",
                ] and
                member not in visited_modules  # not visited yet
            ):
                modules_queue.append(member)
                visited_modules.add(member)
            elif (
                not inspect.ismodule(member) and
                hasattr(member, "__name__") and
                not member.__name__.startswith("_") and
                member.__module__ != module.__name__ and
                member not in visited_functions
            ):
                # skip ufuncs that are exported in np.strings as well
                if member.__name__ in (
                    "add", "equal", "not_equal", "greater", "greater_equal",
                    "less", "less_equal",
                ) and module.__name__ == "numpy.strings":
                    continue

                # recarray and record are exported in np and np.rec
                if (
                    (member.__name__ == "recarray" and module.__name__ == "numpy") or
                    (member.__name__ == "record" and module.__name__ == "numpy.rec")
                ):
                    continue

                # ctypeslib exports ctypes c_long/c_longlong
                if (
                    member.__name__ in ("c_long", "c_longlong") and
                    module.__name__ == "numpy.ctypeslib"
                ):
                    continue

                # skip cdef classes
                if member.__name__ in (
                    "BitGenerator", "Generator", "MT19937", "PCG64", "PCG64DXSM",
                    "Philox", "RandomState", "SFC64", "SeedSequence",
                ):
                    continue

                incorrect_entries.append(
                    {
                        "Func": member.__name__,
                        "actual": member.__module__,
                        "expected": module.__name__,
                    }
                )
                visited_functions.add(member)

    if incorrect_entries:
        assert len(incorrect_entries) == 0, incorrect_entries

