
def save_code(pickler, obj):
    logger.trace(pickler, "Co: %s", obj)
    if hasattr(obj, "co_endlinetable"): # python 3.11a (20 args)
        args = (
            obj.co_lnotab, # for < python 3.10 [not counted in args]
            obj.co_argcount, obj.co_posonlyargcount,
            obj.co_kwonlyargcount, obj.co_nlocals, obj.co_stacksize,
            obj.co_flags, obj.co_code, obj.co_consts, obj.co_names,
            obj.co_varnames, obj.co_filename, obj.co_name, obj.co_qualname,
            obj.co_firstlineno, obj.co_linetable, obj.co_endlinetable,
            obj.co_columntable, obj.co_exceptiontable, obj.co_freevars,
            obj.co_cellvars
        )
    elif hasattr(obj, "co_exceptiontable"): # python 3.11 (18 args)
        with warnings.catch_warnings():
            if not OLD312a7: # issue 597
                warnings.filterwarnings('ignore', category=DeprecationWarning)
            args = (
                obj.co_lnotab, # for < python 3.10 [not counted in args]
                obj.co_argcount, obj.co_posonlyargcount,
                obj.co_kwonlyargcount, obj.co_nlocals, obj.co_stacksize,
                obj.co_flags, obj.co_code, obj.co_consts, obj.co_names,
                obj.co_varnames, obj.co_filename, obj.co_name, obj.co_qualname,
                obj.co_firstlineno, obj.co_linetable, obj.co_exceptiontable,
                obj.co_freevars, obj.co_cellvars
            )
    elif hasattr(obj, "co_qualname"): # pypy 3.11 7.3.19+ (17 args)
        args = (
            obj.co_lnotab, obj.co_argcount, obj.co_posonlyargcount,
            obj.co_kwonlyargcount, obj.co_nlocals, obj.co_stacksize,
            obj.co_flags, obj.co_code, obj.co_consts, obj.co_names,
            obj.co_varnames, obj.co_filename, obj.co_name, obj.co_qualname,
            obj.co_firstlineno, obj.co_linetable, obj.co_freevars,
            obj.co_cellvars
        )
    elif hasattr(obj, "co_linetable"): # python 3.10 (16 args)
        args = (
            obj.co_lnotab, # for < python 3.10 [not counted in args]
            obj.co_argcount, obj.co_posonlyargcount,
            obj.co_kwonlyargcount, obj.co_nlocals, obj.co_stacksize,
            obj.co_flags, obj.co_code, obj.co_consts, obj.co_names,
            obj.co_varnames, obj.co_filename, obj.co_name,
            obj.co_firstlineno, obj.co_linetable, obj.co_freevars,
            obj.co_cellvars
        )
    elif hasattr(obj, "co_posonlyargcount"): # python 3.8 (16 args)
        args = (
            obj.co_argcount, obj.co_posonlyargcount,
            obj.co_kwonlyargcount, obj.co_nlocals, obj.co_stacksize,
            obj.co_flags, obj.co_code, obj.co_consts, obj.co_names,
            obj.co_varnames, obj.co_filename, obj.co_name,
            obj.co_firstlineno, obj.co_lnotab, obj.co_freevars,
            obj.co_cellvars
        )
    else: # python 3.7 (15 args)
        args = (
            obj.co_argcount, obj.co_kwonlyargcount, obj.co_nlocals,
            obj.co_stacksize, obj.co_flags, obj.co_code, obj.co_consts,
            obj.co_names, obj.co_varnames, obj.co_filename,
            obj.co_name, obj.co_firstlineno, obj.co_lnotab,
            obj.co_freevars, obj.co_cellvars
        )

    pickler.save_reduce(_create_code, args, obj=obj)
    logger.trace(pickler, "# Co")
    return

