
def is_optimum_quanto_available():
    return is_optimum_available() and _is_package_available("optimum.quanto")[0]

