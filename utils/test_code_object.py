
def test_code_object():
    import warnings
    from dill._dill import ALL_CODE_PARAMS, CODE_PARAMS, CODE_VERSION, _create_code
    code = function_c.__code__
    warnings.filterwarnings('ignore', category=DeprecationWarning) # issue 597
    LNOTAB = getattr(code, 'co_lnotab', b'')
    if warnings.filters: del warnings.filters[0]
    fields = {f: getattr(code, 'co_'+f) for f in CODE_PARAMS}
    fields.setdefault('posonlyargcount', 0)         # python >= 3.8
    fields.setdefault('lnotab', LNOTAB)             # python <= 3.9
    fields.setdefault('linetable', b'')             # python >= 3.10
    fields.setdefault('qualname', fields['name'])   # python >= 3.11
    fields.setdefault('exceptiontable', b'')        # python >= 3.11
    fields.setdefault('endlinetable', None)         # python == 3.11a
    fields.setdefault('columntable', None)          # python == 3.11a

    for version, _, params in ALL_CODE_PARAMS:
        args = tuple(fields[p] for p in params.split())
        try:
            _create_code(*args)
            if version >= (3,10):
                _create_code(fields['lnotab'], *args)
        except Exception as error:
            raise Exception("failed to construct code object with format version {}".format(version)) from error

