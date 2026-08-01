
def _create_code(*args):
    if not isinstance(args[0], int): # co_lnotab stored from >= 3.10
        LNOTAB, *args = args
    else: # from < 3.10 (or pre-LNOTAB storage)
        LNOTAB = b''

    with match(args) as m:
        # Python 3.11/3.12a (18 members)
        if m.case((
            'argcount', 'posonlyargcount', 'kwonlyargcount', 'nlocals', 'stacksize', 'flags',     # args[0:6]
            'code', 'consts', 'names', 'varnames', 'filename', 'name', 'qualname', 'firstlineno', # args[6:14]
            'linetable', 'exceptiontable', 'freevars', 'cellvars'                                 # args[14:]
        )):
            if CODE_VERSION == (3,11):
                return CodeType(
                    *args[:6],
                    args[6].encode() if hasattr(args[6], 'encode') else args[6], # code
                    *args[7:14],
                    args[14].encode() if hasattr(args[14], 'encode') else args[14], # linetable
                    args[15].encode() if hasattr(args[15], 'encode') else args[15], # exceptiontable
                    args[16],
                    args[17],
                )
            fields = m.fields
        # PyPy 3.11 7.3.19+ (17 members)
        elif m.case((
            'argcount', 'posonlyargcount', 'kwonlyargcount', 'nlocals', 'stacksize', 'flags', # args[0:6]
            'code', 'consts', 'names', 'varnames', 'filename', 'name', 'qualname',            # args[6:13]
            'firstlineno', 'linetable', 'freevars', 'cellvars'                                # args[13:]
        )):
            if CODE_VERSION == (3,11,'p'):
                return CodeType(
                    *args[:6],
                    args[6].encode() if hasattr(args[6], 'encode') else args[6], # code
                    *args[7:14],
                    args[14].encode() if hasattr(args[14], 'encode') else args[14], # linetable
                    args[15],
                    args[16],
                )
            fields = m.fields
        # Python 3.10 or 3.8/3.9 (16 members)
        elif m.case((
            'argcount', 'posonlyargcount', 'kwonlyargcount', 'nlocals', 'stacksize', 'flags', # args[0:6]
            'code', 'consts', 'names', 'varnames', 'filename', 'name', 'firstlineno',         # args[6:13]
            'LNOTAB_OR_LINETABLE', 'freevars', 'cellvars'                                     # args[13:]
        )):
            if CODE_VERSION == (3,10) or CODE_VERSION == (3,8):
                return CodeType(
                    *args[:6],
                    args[6].encode() if hasattr(args[6], 'encode') else args[6], # code
                    *args[7:13],
                    args[13].encode() if hasattr(args[13], 'encode') else args[13], # lnotab/linetable
                    args[14],
                    args[15],
                )
            fields = m.fields
            if CODE_VERSION >= (3,10):
                fields['linetable'] = m.LNOTAB_OR_LINETABLE
            else:
                fields['lnotab'] = LNOTAB if LNOTAB else m.LNOTAB_OR_LINETABLE
        # Python 3.7 (15 args)
        elif m.case((
            'argcount', 'kwonlyargcount', 'nlocals', 'stacksize', 'flags',            # args[0:5]
            'code', 'consts', 'names', 'varnames', 'filename', 'name', 'firstlineno', # args[5:12]
            'lnotab', 'freevars', 'cellvars'                                          # args[12:]
        )):
            if CODE_VERSION == (3,7):
                return CodeType(
                    *args[:5],
                    args[5].encode() if hasattr(args[5], 'encode') else args[5], # code
                    *args[6:12],
                    args[12].encode() if hasattr(args[12], 'encode') else args[12], # lnotab
                    args[13],
                    args[14],
                )
            fields = m.fields
        # Python 3.11a (20 members)
        elif m.case((
            'argcount', 'posonlyargcount', 'kwonlyargcount', 'nlocals', 'stacksize', 'flags',     # args[0:6]
            'code', 'consts', 'names', 'varnames', 'filename', 'name', 'qualname', 'firstlineno', # args[6:14]
            'linetable', 'endlinetable', 'columntable', 'exceptiontable', 'freevars', 'cellvars'  # args[14:]
        )):
            if CODE_VERSION == (3,11,'a'):
                return CodeType(
                    *args[:6],
                    args[6].encode() if hasattr(args[6], 'encode') else args[6], # code
                    *args[7:14],
                    *(a.encode() if hasattr(a, 'encode') else a for a in args[14:18]), # linetable-exceptiontable
                    args[18],
                    args[19],
                )
            fields = m.fields
        else:
            raise UnpicklingError("pattern match for code object failed")

    # The args format doesn't match this version.
    fields.setdefault('posonlyargcount', 0)         # from python <= 3.7
    fields.setdefault('lnotab', LNOTAB)             # from python >= 3.10
    fields.setdefault('linetable', b'')             # from python <= 3.9
    fields.setdefault('qualname', fields['name'])   # from python <= 3.10
    fields.setdefault('exceptiontable', b'')        # from python <= 3.10
    fields.setdefault('endlinetable', None)         # from python != 3.11a
    fields.setdefault('columntable', None)          # from python != 3.11a

    args = (fields[k].encode() if k in ENCODE_PARAMS and hasattr(fields[k], 'encode') else fields[k]
            for k in CODE_PARAMS)
    return CodeType(*args)

