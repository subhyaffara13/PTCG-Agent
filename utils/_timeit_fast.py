
def _timeit_fast(stmt="pass", setup="pass", repeat=3):
    """
    Returns the time the statement/function took, in seconds.

    Faster, less precise version of IPython's timeit. `stmt` can be a statement
    written as a string or a callable.

    Will do only 1 loop (like IPython's timeit) with no repetitions
    (unlike IPython) for very slow functions.  For fast functions, only does
    enough loops to take 5 ms, which seems to produce similar results (on
    Windows at least), and avoids doing an extraneous cycle that isn't
    measured.

    """
    timer = timeit.Timer(stmt, setup)

    # determine number of calls per rep so total time for 1 rep >= 5 ms
    x = 0
    for p in range(0, 10):
        number = 10**p
        x = timer.timeit(number)  # seconds
        if x >= 5e-3 / 10:  # 5 ms for final test, 1/10th that for this one
            break
    if x > 1:  # second
        # If it's macroscopic, don't bother with repetitions
        best = x
    else:
        number *= 10
        r = timer.repeat(repeat, number)
        best = min(r)

    sec = best / number
    return sec

