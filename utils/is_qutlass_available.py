
def is_qutlass_available():
    is_available, qutlass_version = _is_package_available("qutlass", return_version=True)
    return is_available and version.parse(qutlass_version) >= version.parse("0.2.0")

