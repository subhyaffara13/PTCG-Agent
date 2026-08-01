
def __do_timings():
    import os
    res = os.getenv('SYMPY_TIMINGS', '')
    res = [x.strip() for x in res.split(',')]
    return set(res)

