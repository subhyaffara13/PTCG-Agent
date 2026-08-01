
def check_unspec_python_args(args: Iterable[Any], kwargs: Mapping[Any, Any]) -> bool:
    from .variables import VariableTracker
    from .variables.tensor import UnspecializedPythonVariable

    unspec_count = 0
    for x in itertools.chain(args, kwargs.values()):
        if isinstance(x, UnspecializedPythonVariable):
            unspec_count += 1
        elif not (isinstance(x, VariableTracker) and x.is_python_constant()):
            return False
    return unspec_count > 0

