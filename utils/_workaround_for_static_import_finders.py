
def _workaround_for_static_import_finders():
    # Issue #392: packaging tools like cx_Freeze can not find these
    # because pycparser uses exec dynamic import.  This is an obscure
    # workaround.  This function is never called.
    import pycparser.yacctab
    import pycparser.lextab

