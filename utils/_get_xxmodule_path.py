
def _get_xxmodule_path():
    source_name = 'xxmodule.c' if sys.version_info > (3, 9) else 'xxmodule-3.8.c'
    return os.path.join(os.path.dirname(__file__), source_name)

