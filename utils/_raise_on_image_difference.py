import os

def _raise_on_image_difference(expected, actual, tol):
    __tracebackhide__ = True

    err = compare_images(expected, actual, tol, in_decorator=True)
    if err:
        for key in ["actual", "expected", "diff"]:
            err[key] = os.path.relpath(err[key])
        raise ImageComparisonFailure(
            ('images not close (RMS %(rms).3f):'
                '\n\t%(actual)s\n\t%(expected)s\n\t%(diff)s') % err)

