import sys

def _trim_arity(func, max_limit=3):
    """decorator to trim function calls to match the arity of the target"""
    global _trim_arity_call_line, pa_call_line_synth

    if func in _single_arg_builtins:
        return lambda s, l, t: func(t)

    limit = 0
    found_arity = False

    # synthesize what would be returned by traceback.extract_stack at the call to
    # user's parse action 'func', so that we don't incur call penalty at parse time

    # fmt: off
    LINE_DIFF = 9
    # IF ANY CODE CHANGES, EVEN JUST COMMENTS OR BLANK LINES, BETWEEN THE NEXT LINE AND
    # THE CALL TO FUNC INSIDE WRAPPER, LINE_DIFF MUST BE MODIFIED!!!!
    _trim_arity_call_line = _trim_arity_call_line or traceback.extract_stack(limit=2)[-1]
    pa_call_line_synth = pa_call_line_synth or (_trim_arity_call_line[0], _trim_arity_call_line[1] + LINE_DIFF)

    def wrapper(*args):
        nonlocal found_arity, limit
        if found_arity:
            return func(*args[limit:])
        while 1:
            try:
                ret = func(*args[limit:])
                found_arity = True
                return ret
            except TypeError as te:
                # re-raise TypeErrors if they did not come from our arity testing
                if found_arity:
                    raise
                else:
                    tb = te.__traceback__
                    frames = traceback.extract_tb(tb, limit=2)
                    frame_summary = frames[-1]
                    trim_arity_type_error = (
                        [frame_summary[:2]][-1][:2] == pa_call_line_synth
                    )
                    del tb

                    if trim_arity_type_error:
                        if limit < max_limit:
                            limit += 1
                            continue

                    raise
            except IndexError as ie:
                # wrap IndexErrors inside a _ParseActionIndexError
                raise _ParseActionIndexError(
                    "IndexError raised in parse action", ie
                ).with_traceback(None)
    # fmt: on

    # copy func name to wrapper for sensible debug output
    # (can't use functools.wraps, since that messes with function signature)
    func_name = getattr(func, "__name__", getattr(func, "__class__").__name__)
    wrapper.__name__ = func_name
    wrapper.__doc__ = func.__doc__

    return wrapper


def _trim_arity(func, maxargs=2):
    if func in singleArgBuiltins:
        return lambda s, l, t: func(t)
    limit = [0]
    foundArity = [False]

    # traceback return data structure changed in Py3.5 - normalize back to plain tuples
    if system_version[:2] >= (3, 5):
        def extract_stack(limit=0):
            # special handling for Python 3.5.0 - extra deep call stack by 1
            offset = -3 if system_version == (3, 5, 0) else -2
            frame_summary = traceback.extract_stack(limit=-offset + limit - 1)[offset]
            return [frame_summary[:2]]
        def extract_tb(tb, limit=0):
            frames = traceback.extract_tb(tb, limit=limit)
            frame_summary = frames[-1]
            return [frame_summary[:2]]
    else:
        extract_stack = traceback.extract_stack
        extract_tb = traceback.extract_tb

    # synthesize what would be returned by traceback.extract_stack at the call to
    # user's parse action 'func', so that we don't incur call penalty at parse time

    LINE_DIFF = 6
    # IF ANY CODE CHANGES, EVEN JUST COMMENTS OR BLANK LINES, BETWEEN THE NEXT LINE AND
    # THE CALL TO FUNC INSIDE WRAPPER, LINE_DIFF MUST BE MODIFIED!!!!
    this_line = extract_stack(limit=2)[-1]
    pa_call_line_synth = (this_line[0], this_line[1] + LINE_DIFF)

    def wrapper(*args):
        while 1:
            try:
                ret = func(*args[limit[0]:])
                foundArity[0] = True
                return ret
            except TypeError:
                # re-raise TypeErrors if they did not come from our arity testing
                if foundArity[0]:
                    raise
                else:
                    try:
                        tb = sys.exc_info()[-1]
                        if not extract_tb(tb, limit=2)[-1][:2] == pa_call_line_synth:
                            raise
                    finally:
                        try:
                            del tb
                        except NameError:
                            pass

                if limit[0] <= maxargs:
                    limit[0] += 1
                    continue
                raise

    # copy func name to wrapper for sensible debug output
    func_name = "<parse action>"
    try:
        func_name = getattr(func, '__name__',
                            getattr(func, '__class__').__name__)
    except Exception:
        func_name = str(func)
    wrapper.__name__ = func_name

    return wrapper

