
def _code_reduce(obj):
    """code object reducer."""
    # If you are not sure about the order of arguments, take a look at help
    # of the specific type from types, for example:
    # >>> from types import CodeType
    # >>> help(CodeType)

    # Hack to circumvent non-predictable memoization caused by string interning.
    # See the inline comment in _class_setstate for details.
    co_name = "".join(obj.co_name)

    # Create shallow copies of these tuple to make cloudpickle payload deterministic.
    # When creating a code object during load, copies of these four tuples are
    # created, while in the main process, these tuples can be shared.
    # By always creating copies, we make sure the resulting payload is deterministic.
    co_names = tuple(name for name in obj.co_names)
    co_varnames = tuple(name for name in obj.co_varnames)
    co_freevars = tuple(name for name in obj.co_freevars)
    co_cellvars = tuple(name for name in obj.co_cellvars)
    if hasattr(obj, "co_exceptiontable"):
        # Python 3.11 and later: there are some new attributes
        # related to the enhanced exceptions.
        args = (
            obj.co_argcount,
            obj.co_posonlyargcount,
            obj.co_kwonlyargcount,
            obj.co_nlocals,
            obj.co_stacksize,
            obj.co_flags,
            obj.co_code,
            obj.co_consts,
            co_names,
            co_varnames,
            obj.co_filename,
            co_name,
            obj.co_qualname,
            obj.co_firstlineno,
            obj.co_linetable,
            obj.co_exceptiontable,
            co_freevars,
            co_cellvars,
        )
    elif hasattr(obj, "co_linetable"):
        # Python 3.10 and later: obj.co_lnotab is deprecated and constructor
        # expects obj.co_linetable instead.
        args = (
            obj.co_argcount,
            obj.co_posonlyargcount,
            obj.co_kwonlyargcount,
            obj.co_nlocals,
            obj.co_stacksize,
            obj.co_flags,
            obj.co_code,
            obj.co_consts,
            co_names,
            co_varnames,
            obj.co_filename,
            co_name,
            obj.co_firstlineno,
            obj.co_linetable,
            co_freevars,
            co_cellvars,
        )
    elif hasattr(obj, "co_nmeta"):  # pragma: no cover
        # "nogil" Python: modified attributes from 3.9
        args = (
            obj.co_argcount,
            obj.co_posonlyargcount,
            obj.co_kwonlyargcount,
            obj.co_nlocals,
            obj.co_framesize,
            obj.co_ndefaultargs,
            obj.co_nmeta,
            obj.co_flags,
            obj.co_code,
            obj.co_consts,
            co_varnames,
            obj.co_filename,
            co_name,
            obj.co_firstlineno,
            obj.co_lnotab,
            obj.co_exc_handlers,
            obj.co_jump_table,
            co_freevars,
            co_cellvars,
            obj.co_free2reg,
            obj.co_cell2reg,
        )
    else:
        # Backward compat for 3.8 and 3.9
        args = (
            obj.co_argcount,
            obj.co_posonlyargcount,
            obj.co_kwonlyargcount,
            obj.co_nlocals,
            obj.co_stacksize,
            obj.co_flags,
            obj.co_code,
            obj.co_consts,
            co_names,
            co_varnames,
            obj.co_filename,
            co_name,
            obj.co_firstlineno,
            obj.co_lnotab,
            co_freevars,
            co_cellvars,
        )
    return types.CodeType, args

