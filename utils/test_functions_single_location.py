
def test_functions_single_location():
    """
    Check that each public function is available from one location only.

    Test performs BFS search traversing NumPy's public API. It flags
    any function-like object that is accessible from more that one place.
    """
    from collections.abc import Callable
    from typing import Any

    from numpy._core._multiarray_umath import (
        _ArrayFunctionDispatcher as dispatched_function,
    )

    visited_modules: set[types.ModuleType] = {np}
    visited_functions: set[Callable[..., Any]] = set()
    # Functions often have `__name__` overridden, therefore we need
    # to keep track of locations where functions have been found.
    functions_original_paths: dict[Callable[..., Any], str] = {}

    # Here we aggregate functions with more than one location.
    # It must be empty for the test to pass.
    duplicated_functions: list[tuple] = []

    modules_queue = [np]

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
                # not a legacy or testing module
                member_name not in ["f2py", "ma", "testing", "tests"] and
                member not in visited_modules  # not visited yet
            ):
                modules_queue.append(member)
                visited_modules.add(member)

            # else check if we got a function-like object
            elif (
                inspect.isfunction(member) or
                isinstance(member, (dispatched_function, np.ufunc))
            ):
                if member in visited_functions:

                    # skip main namespace functions with aliases
                    if (
                        member.__name__ in [
                            "absolute",  # np.abs
                            "arccos",  # np.acos
                            "arccosh",  # np.acosh
                            "arcsin",  # np.asin
                            "arcsinh",  # np.asinh
                            "arctan",  # np.atan
                            "arctan2",  # np.atan2
                            "arctanh",  # np.atanh
                            "left_shift",  # np.bitwise_left_shift
                            "right_shift",  # np.bitwise_right_shift
                            "conjugate",  # np.conj
                            "invert",  # np.bitwise_not & np.bitwise_invert
                            "remainder",  # np.mod
                            "divide",  # np.true_divide
                            "concatenate",  # np.concat
                            "power",  # np.pow
                            "transpose",  # np.permute_dims
                        ] and
                        module.__name__ == "numpy"
                    ):
                        continue
                    # skip trimcoef from numpy.polynomial as it is
                    # duplicated by design.
                    if (
                        member.__name__ == "trimcoef" and
                        module.__name__.startswith("numpy.polynomial")
                    ):
                        continue

                    # skip ufuncs that are exported in np.strings as well
                    if member.__name__ in (
                        "add",
                        "equal",
                        "not_equal",
                        "greater",
                        "greater_equal",
                        "less",
                        "less_equal",
                    ) and module.__name__ == "numpy.strings":
                        continue

                    # numpy.char reexports all numpy.strings functions for
                    # backwards-compatibility
                    if module.__name__ == "numpy.char":
                        continue

                    # function is present in more than one location!
                    duplicated_functions.append(
                        (member.__name__,
                         module.__name__,
                         functions_original_paths[member])
                    )
                else:
                    visited_functions.add(member)
                    functions_original_paths[member] = module.__name__

    del visited_functions, visited_modules, functions_original_paths

    assert len(duplicated_functions) == 0, duplicated_functions

