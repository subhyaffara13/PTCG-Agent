
def _unpack_LinregressResult(res, _):
    return tuple(res) + (res.intercept_stderr,)

