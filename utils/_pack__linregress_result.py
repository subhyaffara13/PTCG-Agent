
def _pack_LinregressResult(slope, intercept, rvalue, pvalue, stderr, intercept_stderr):
    return LinregressResult(slope, intercept, rvalue, pvalue, stderr,
                            intercept_stderr=intercept_stderr)

