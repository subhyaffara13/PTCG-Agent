
def _replace_heap(variable, heap):

    if isinstance(variable, Pointer):

        while isinstance(variable, Pointer):

            if variable.index == 0:
                variable = None
            else:
                if variable.index in heap:
                    variable = heap[variable.index]
                else:
                    warnings.warn("Variable referenced by pointer not found "
                                  "in heap: variable will be set to None",
                                  stacklevel=3)
                    variable = None

        replace, new = _replace_heap(variable, heap)

        if replace:
            variable = new

        return True, variable

    elif isinstance(variable, np.rec.recarray):

        # Loop over records
        for ir, record in enumerate(variable):

            replace, new = _replace_heap(record, heap)

            if replace:
                variable[ir] = new

        return False, variable

    elif isinstance(variable, np.record):

        # Loop over values
        for iv, value in enumerate(variable):

            replace, new = _replace_heap(value, heap)

            if replace:
                variable[iv] = new

        return False, variable

    elif isinstance(variable, np.ndarray):

        # Loop over values if type is np.object_
        if variable.dtype.type is np.object_:

            for iv in range(variable.size):

                replace, new = _replace_heap(variable.item(iv), heap)

                if replace:
                    variable.reshape(-1)[iv] = new

        return False, variable

    else:

        return False, variable

