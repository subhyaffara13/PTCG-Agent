
def _dispatch(table, min, max=None, state=None, args=('raw',)):
    """
    Decorator for dispatch by opcode. Sets the values in *table*
    from *min* to *max* to this method, adds a check that the Dvi state
    matches *state* if not None, reads arguments from the file according
    to *args*.

    Parameters
    ----------
    table : dict[int, callable]
        The dispatch table to be filled in.

    min, max : int
        Range of opcodes that calls the registered function; *max* defaults to
        *min*.

    state : _dvistate, optional
        State of the Dvi object in which these opcodes are allowed.

    args : list[str], default: ['raw']
        Sequence of argument specifications:

        - 'raw': opcode minus minimum
        - 'u1': read one unsigned byte
        - 'u4': read four bytes, treat as an unsigned number
        - 's4': read four bytes, treat as a signed number
        - 'slen': read (opcode - minimum) bytes, treat as signed
        - 'slen1': read (opcode - minimum + 1) bytes, treat as signed
        - 'ulen1': read (opcode - minimum + 1) bytes, treat as unsigned
        - 'olen1': read (opcode - minimum + 1) bytes, treat as unsigned
          if under four bytes, signed if four bytes
    """
    def decorate(method):
        get_args = [_arg_mapping[x] for x in args]

        @wraps(method)
        def wrapper(self, byte):
            if state is not None and self.state != state:
                raise ValueError("state precondition failed")
            return method(self, *[f(self, byte-min) for f in get_args])
        if max is None:
            table[min] = wrapper
        else:
            for i in range(min, max+1):
                assert table[i] is None
                table[i] = wrapper
        return wrapper
    return decorate


def _dispatch(func):
    """
    Function annotation that creates a uarray multimethod from the function
    """
    return generate_multimethod(func, _x_replacer, domain="numpy.scipy.fft")


def _dispatch(f):
    # For each public method (instance function) of a distribution (e.g. ccdf),
    # there may be several ways ("method"s) that it can be computed (e.g. a
    # formula, as the complement of the CDF, or via numerical integration).
    # Each "method" is implemented by a different private method (instance
    # function).
    # This wrapper calls the appropriate private method based on the public
    # method and any specified `method` keyword option.
    # - If `method` is specified as a string (by the user), the appropriate
    #   private method is called.
    # - If `method` is None:
    #   - The appropriate private method for the public method is looked up
    #     in a cache.
    #   - If the cache does not have an entry for the public method, the
    #     appropriate "dispatch " function is called to determine which method
    #     is most appropriate given the available private methods and
    #     settings (e.g. tolerance).

    @functools.wraps(f)
    def wrapped(self, *args, method=None, **kwargs):
        func_name = f.__name__
        method = method or self._method_cache.get(func_name, None)
        if callable(method):
            pass
        elif method is not None:
            method = 'logexp' if method == 'log/exp' else method
            method_name = func_name.replace('dispatch', method)
            method = getattr(self, method_name)
        else:
            method = f(self, *args, method=method, **kwargs)
            if func_name != '_sample_dispatch' and self.cache_policy != _NO_CACHE:
                self._method_cache[func_name] = method

        try:
            return method(*args, **kwargs)
        except KeyError as e:
            raise NotImplementedError(self._not_implemented) from e

    return wrapped

