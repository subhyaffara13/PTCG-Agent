
def _save_with_postproc(pickler, reduction, is_pickler_dill=None, obj=Getattr.NO_DEFAULT, postproc_list=None):
    if obj is Getattr.NO_DEFAULT:
        obj = Reduce(reduction) # pragma: no cover

    if is_pickler_dill is None:
        is_pickler_dill = is_dill(pickler, child=True)
    if is_pickler_dill:
        # assert id(obj) not in pickler._postproc, str(obj) + ' already pushed on stack!'
        # if not hasattr(pickler, 'x'): pickler.x = 0
        # print(pickler.x*' ', 'push', obj, id(obj), pickler._recurse)
        # pickler.x += 1
        if postproc_list is None:
            postproc_list = []

        # Recursive object not supported. Default to a global instead.
        if id(obj) in pickler._postproc:
            name = '%s.%s ' % (obj.__module__, getattr(obj, '__qualname__', obj.__name__)) if hasattr(obj, '__module__') else ''
            warnings.warn('Cannot pickle %r: %shas recursive self-references that trigger a RecursionError.' % (obj, name), PicklingWarning)
            pickler.save_global(obj)
            return
        pickler._postproc[id(obj)] = postproc_list

    # TODO: Use state_setter in Python 3.8 to allow for faster cPickle implementations
    pickler.save_reduce(*reduction, obj=obj)

    if is_pickler_dill:
        # pickler.x -= 1
        # print(pickler.x*' ', 'pop', obj, id(obj))
        postproc = pickler._postproc.pop(id(obj))
        # assert postproc_list == postproc, 'Stack tampered!'
        for reduction in reversed(postproc):
            if reduction[0] is _setitems:
                # use the internal machinery of pickle.py to speedup when
                # updating a dictionary in postproc
                dest, source = reduction[1]
                if source:
                    pickler.write(pickler.get(pickler.memo[id(dest)][0]))
                    if sys.hexversion < 0x30e00a1:
                        pickler._batch_setitems(iter(source.items()))
                    else:
                        pickler._batch_setitems(iter(source.items()), obj=obj)
                else:
                    # Updating with an empty dictionary. Same as doing nothing.
                    continue
            else:
                pickler.save_reduce(*reduction)
            # pop None created by calling preprocessing step off stack
            pickler.write(POP)

