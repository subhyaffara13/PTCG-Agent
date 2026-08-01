
def save_function(pickler, obj):
    if not _locate_function(obj, pickler):
        if type(obj.__code__) is not CodeType:
            # Some PyPy builtin functions have no module name, and thus are not
            # able to be located
            module_name = getattr(obj, '__module__', None)
            if module_name is None:
                module_name = __builtin__.__name__
            module = _import_module(module_name, safe=True)
            _pypy_builtin = False
            try:
                found, _ = _getattribute(module, obj.__qualname__)
                if getattr(found, '__func__', None) is obj:
                    _pypy_builtin = True
            except AttributeError:
                pass

            if _pypy_builtin:
                logger.trace(pickler, "F3: %s", obj)
                pickler.save_reduce(getattr, (found, '__func__'), obj=obj)
                logger.trace(pickler, "# F3")
                return

        logger.trace(pickler, "F1: %s", obj)
        _recurse = getattr(pickler, '_recurse', None)
        _postproc = getattr(pickler, '_postproc', None)
        _main_modified = getattr(pickler, '_main_modified', None)
        _original_main = getattr(pickler, '_original_main', __builtin__)#'None'
        postproc_list = []
        if _recurse:
            # recurse to get all globals referred to by obj
            from .detect import globalvars
            globs_copy = globalvars(obj, recurse=True, builtin=True)

            # Add the name of the module to the globs dictionary to prevent
            # the duplication of the dictionary. Pickle the unpopulated
            # globals dictionary and set the remaining items after the function
            # is created to correctly handle recursion.
            globs = {'__name__': obj.__module__}
        else:
            globs_copy = obj.__globals__

            # If the globals is the __dict__ from the module being saved as a
            # session, substitute it by the dictionary being actually saved.
            if _main_modified and globs_copy is _original_main.__dict__:
                globs_copy = getattr(pickler, '_main', _original_main).__dict__
                globs = globs_copy
            # If the globals is a module __dict__, do not save it in the pickle.
            elif globs_copy is not None and obj.__module__ is not None and \
                    getattr(_import_module(obj.__module__, True), '__dict__', None) is globs_copy:
                globs = globs_copy
            else:
                globs = {'__name__': obj.__module__}

        if globs_copy is not None and globs is not globs_copy:
            # In the case that the globals are copied, we need to ensure that
            # the globals dictionary is updated when all objects in the
            # dictionary are already created.
            glob_ids = {id(g) for g in globs_copy.values()}
            for stack_element in _postproc:
                if stack_element in glob_ids:
                    _postproc[stack_element].append((_setitems, (globs, globs_copy)))
                    break
            else:
                postproc_list.append((_setitems, (globs, globs_copy)))

        closure = obj.__closure__
        state_dict = {}
        for fattrname in ('__doc__', '__kwdefaults__', '__annotations__'):
            fattr = getattr(obj, fattrname, None)
            if fattr is not None:
                state_dict[fattrname] = fattr
        if obj.__qualname__ != obj.__name__:
            state_dict['__qualname__'] = obj.__qualname__
        if '__name__' not in globs or obj.__module__ != globs['__name__']:
            state_dict['__module__'] = obj.__module__

        state = obj.__dict__
        if type(state) is not dict:
            state_dict['__dict__'] = state
            state = None
        if state_dict:
            state = state, state_dict

        _save_with_postproc(pickler, (_create_function, (
                obj.__code__, globs, obj.__name__, obj.__defaults__,
                closure
        ), state), obj=obj, postproc_list=postproc_list)

        # Lift closure cell update to earliest function (#458)
        if _postproc:
            topmost_postproc = next(iter(_postproc.values()), None)
            if closure and topmost_postproc:
                for cell in closure:
                    possible_postproc = (setattr, (cell, 'cell_contents', obj))
                    try:
                        topmost_postproc.remove(possible_postproc)
                    except ValueError:
                        continue

                    # Change the value of the cell
                    pickler.save_reduce(*possible_postproc)
                    # pop None created by calling preprocessing step off stack
                    pickler.write(POP)

        logger.trace(pickler, "# F1")
    else:
        logger.trace(pickler, "F2: %s", obj)
        name = getattr(obj, '__qualname__', getattr(obj, '__name__', None))
        StockPickler.save_global(pickler, obj, name=name)
        logger.trace(pickler, "# F2")
    return

