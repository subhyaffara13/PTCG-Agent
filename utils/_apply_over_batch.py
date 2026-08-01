
def _apply_over_batch(*argdefs):
    """
    Factory for decorator that applies a function over batched arguments.

    Array arguments may have any number of core dimensions (typically 0,
    1, or 2) and any broadcastable batch shapes. There may be any
    number of array outputs of any number of dimensions. Assumptions
    right now - which are satisfied by all functions of interest in `linalg` -
    are that all array inputs are consecutive keyword or positional arguments,
    and that the wrapped function returns either a single array or a tuple of
    arrays. It's only as general as it needs to be right now - it can be extended.

    Parameters
    ----------
    *argdefs : tuple of (str, int)
        Definitions of array arguments: the keyword name of the argument, and
        the number of core dimensions.

    Example:
    --------
    `linalg.eig` accepts two matrices as the first two arguments `a` and `b`, where
    `b` is optional, and returns one array or a tuple of arrays, depending on the
    values of other positional or keyword arguments. To generate a wrapper that applies
    the function over batches of `a` and optionally `b` :

    >>> _apply_over_batch(('a', 2), ('b', 2))
    """
    names, ndims = list(zip(*argdefs))
    n_arrays = len(names)

    def decorator(f):
        @functools.wraps(f)
        def wrapper(*args, **kwargs):
            args = list(args)

            # Ensure all arrays in `arrays`, other arguments in `other_args`/`kwargs`
            arrays, other_args = args[:n_arrays], args[n_arrays:]
            for i, name in enumerate(names):
                if name in kwargs:
                    if i + 1 <= len(args):
                        raise ValueError(f'{f.__name__}() got multiple values '
                                         f'for argument `{name}`.')
                    else:
                        arrays.append(kwargs.pop(name))

            xp = array_namespace(*arrays)

            # Determine core and batch shapes
            batch_shapes = []
            core_shapes = []
            for i, (array, ndim) in enumerate(zip(arrays, ndims)):
                array = None if array is None else xp.asarray(array)
                shape = () if array is None else array.shape

                if ndim == "1|2":  # special case for `solve`, etc.
                    ndim = 2 if array.ndim >= 2 else 1

                arrays[i] = array
                batch_shapes.append(shape[:-ndim] if ndim > 0 else shape)
                core_shapes.append(shape[-ndim:] if ndim > 0 else ())

            # complain on dtypes
            if is_numpy(xp):
                _deprecate_dtypes(f.__name__, *arrays)

            # Early exit if call is not batched
            if not any(batch_shapes):
                return f(*arrays, *other_args, **kwargs)

            # Determine broadcasted batch shape
            batch_shape = np.broadcast_shapes(*batch_shapes)  # Gives OK error message

            # We can't support zero-size batches right now because without data with
            # which to call the function, the decorator doesn't even know the *number*
            # of outputs, let alone their core shapes or dtypes.
            if math.prod(batch_shape) == 0:
                message = f'`{f.__name__}` does not support zero-size batches.'
                raise ValueError(message)

            # Broadcast arrays to appropriate shape
            for i, (array, core_shape) in enumerate(zip(arrays, core_shapes)):
                if array is None:
                    continue
                arrays[i] = xp.broadcast_to(array, batch_shape + core_shape)

            # Main loop
            results = []
            for index in np.ndindex(batch_shape):
                result = f(*((array[index] if array is not None else None)
                             for array in arrays), *other_args, **kwargs)
                # Assume `result` is either a tuple or single array. This is easily
                # generalized by allowing the contributor to pass an `unpack_result`
                # callable to the decorator factory.
                result = (result,) if not isinstance(result, tuple) else result
                results.append(result)
            results = list(zip(*results))

            # Reshape results
            for i, result in enumerate(results):
                result = xp.stack(result)
                core_shape = result.shape[1:]
                results[i] = xp.reshape(result, batch_shape + core_shape)

            # Assume `result` should be a single array if there is only one element or
            # a `tuple` otherwise. This is easily generalized by allowing the
            # contributor to pass an `pack_result` callable to the decorator factory.
            return results[0] if len(results) == 1 else results

        doc = FunctionDoc(wrapper)
        doc['Extended Summary'].append(_batch_note.rstrip())
        wrapper.__doc__ = str(doc).split("\n", 1)[1].lstrip(" \n")  # remove signature

        return wrapper
    return decorator

