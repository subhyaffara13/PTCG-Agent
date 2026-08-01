
def save_cell(pickler, obj):
    try:
        f = obj.cell_contents
    except ValueError: # cell is empty
        logger.trace(pickler, "Ce3: %s", obj)
        # _shims._CELL_EMPTY is defined in _shims.py to support PyPy 2.7.
        # It unpickles to a sentinel object _dill._CELL_EMPTY, also created in
        # _shims.py. This object is not present in Python 3 because the cell's
        # contents can be deleted in newer versions of Python. The reduce object
        # will instead unpickle to None if unpickled in Python 3.

        # When breaking changes are made to dill, (_shims._CELL_EMPTY,) can
        # be replaced by () OR the delattr function can be removed repending on
        # whichever is more convienient.
        pickler.save_reduce(_create_cell, (_shims._CELL_EMPTY,), obj=obj)
        # Call the function _delattr on the cell's cell_contents attribute
        # The result of this function call will be None
        pickler.save_reduce(_shims._delattr, (obj, 'cell_contents'))
        # pop None created by calling _delattr off stack
        pickler.write(POP)
        logger.trace(pickler, "# Ce3")
        return
    if is_dill(pickler, child=True):
        if id(f) in pickler._postproc:
            # Already seen. Add to its postprocessing.
            postproc = pickler._postproc[id(f)]
        else:
            # Haven't seen it. Add to the highest possible object and set its
            # value as late as possible to prevent cycle.
            postproc = next(iter(pickler._postproc.values()), None)
        if postproc is not None:
            logger.trace(pickler, "Ce2: %s", obj)
            # _CELL_REF is defined in _shims.py to support older versions of
            # dill. When breaking changes are made to dill, (_CELL_REF,) can
            # be replaced by ()
            pickler.save_reduce(_create_cell, (_CELL_REF,), obj=obj)
            postproc.append((_shims._setattr, (obj, 'cell_contents', f)))
            logger.trace(pickler, "# Ce2")
            return
    logger.trace(pickler, "Ce1: %s", obj)
    pickler.save_reduce(_create_cell, (f,), obj=obj)
    logger.trace(pickler, "# Ce1")
    return

