
def get_py_files():
    return [p for p in ROOT.rglob('*.py') if p.is_file()]

