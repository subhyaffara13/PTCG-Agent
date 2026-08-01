
def _is_valid_engine_ext_pair(engine, read_ext: str) -> bool:
    """
    Filter out invalid (engine, ext) pairs instead of skipping, as that
    produces 500+ pytest.skips.
    """
    engine = engine.values[0]
    if engine == "openpyxl" and read_ext == ".xls":
        return False
    if engine == "odf" and read_ext != ".ods":
        return False
    if read_ext == ".ods" and engine not in {"odf", "calamine"}:
        return False
    if engine == "pyxlsb" and read_ext != ".xlsb":
        return False
    if read_ext == ".xlsb" and engine not in {"pyxlsb", "calamine"}:
        return False
    if engine == "xlrd" and read_ext != ".xls":
        return False
    return True

