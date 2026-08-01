
def checkPath(filename, reporter=None):
    """
    Check the given path, printing out any warnings detected.

    @param reporter: A L{Reporter} instance, where errors and warnings will be
        reported.

    @return: the number of warnings printed
    """
    if reporter is None:
        reporter = modReporter._makeDefaultReporter()
    try:
        with open(filename, 'rb') as f:
            codestr = f.read()
    except OSError as e:
        reporter.unexpectedError(filename, e.args[1])
        return 1
    return check(codestr, filename, reporter)


def check_path(test_output: PathType, benchmark: PathType, bypass: bool = False) -> bool:
    if not isinstance(test_output, list):
        return False

    if len(test_output) != len(benchmark):
        return False

    ret = True
    for pos in range(len(test_output)):
        ret &= isinstance(test_output[pos], tuple)
        ret &= test_output[pos] == list(benchmark)[pos]
    return ret


def check_path(board, start, dirs, dist_a, dist_b, collection_rate):
    kore = 0
    npv = 0.98
    current = start
    steps = 2 * (dist_a + dist_b + 2)
    for idx, d in enumerate(dirs):
        for _ in range((dist_a if idx % 2 == 0 else dist_b) + 1):
            current = current.translate(d.to_point(), board.configuration.size)
            kore += int((board.cells.get(current).kore or 0) * collection_rate)
    return math.pow(npv, steps) * kore / (2 * (dist_a + dist_b + 2))

