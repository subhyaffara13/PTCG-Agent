
def is_fp_quant_available():
    is_available, fp_quant_version = _is_package_available("fp_quant", return_version=True)
    return is_available and version.parse(fp_quant_version) >= version.parse("0.3.2")

