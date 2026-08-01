
def _caller_dir_pycache():
    if _TMPDIR:
        return _TMPDIR
    result = os.environ.get('CFFI_TMPDIR')
    if result:
        return result
    filename = sys._getframe(2).f_code.co_filename
    return os.path.abspath(os.path.join(os.path.dirname(filename),
                           '__pycache__'))

