import sys

def register_pickle_by_value(module):
    """Register a module to make its functions and classes picklable by value.

    By default, functions and classes that are attributes of an importable
    module are to be pickled by reference, that is relying on re-importing
    the attribute from the module at load time.

    If `register_pickle_by_value(module)` is called, all its functions and
    classes are subsequently to be pickled by value, meaning that they can
    be loaded in Python processes where the module is not importable.

    This is especially useful when developing a module in a distributed
    execution environment: restarting the client Python process with the new
    source code is enough: there is no need to re-install the new version
    of the module on all the worker nodes nor to restart the workers.

    Note: this feature is considered experimental. See the cloudpickle
    README.md file for more details and limitations.
    """
    if not isinstance(module, types.ModuleType):
        raise ValueError(f"Input should be a module object, got {str(module)} instead")
    # In the future, cloudpickle may need a way to access any module registered
    # for pickling by value in order to introspect relative imports inside
    # functions pickled by value. (see
    # https://github.com/cloudpipe/cloudpickle/pull/417#issuecomment-873684633).
    # This access can be ensured by checking that module is present in
    # sys.modules at registering time and assuming that it will still be in
    # there when accessed during pickling. Another alternative would be to
    # store a weakref to the module. Even though cloudpickle does not implement
    # this introspection yet, in order to avoid a possible breaking change
    # later, we still enforce the presence of module inside sys.modules.
    if module.__name__ not in sys.modules:
        raise ValueError(
            f"{module} was not imported correctly, have you used an "
            "`import` statement to access it?"
        )
    _PICKLE_BY_VALUE_MODULES.add(module.__name__)

