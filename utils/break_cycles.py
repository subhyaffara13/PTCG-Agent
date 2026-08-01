
def break_cycles():
    """
    Break reference cycles by calling gc.collect
    Objects can call other objects' methods (for instance, another object's
     __del__) inside their own __del__. On PyPy, the interpreter only runs
    between calls to gc.collect, so multiple calls are needed to completely
    release all cycles.
    """

    gc.collect()
    if IS_PYPY:
        # a few more, just to make sure all the finalizers are called
        gc.collect()
        gc.collect()
        gc.collect()
        gc.collect()


def break_cycles():
    """
    Break reference cycles by calling gc.collect
    Objects can call other objects' methods (for instance, another object's
     __del__) inside their own __del__. On PyPy, the interpreter only runs
    between calls to gc.collect, so multiple calls are needed to completely
    release all cycles.
    """

    gc.collect()
    if IS_PYPY:
        # a few more, just to make sure all the finalizers are called
        gc.collect()
        gc.collect()
        gc.collect()
        gc.collect()

