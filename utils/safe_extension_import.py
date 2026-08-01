
def safe_extension_import(name, path):
    with import_helper.CleanImport(name):
        with extension_redirect(name, path) as new_path:
            with import_helper.DirsOnSysPath(new_path):
                yield

