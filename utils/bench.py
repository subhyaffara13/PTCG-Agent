import os

def bench(strictio, fmode, skippypy):
    import platform
    if skippypy and platform.python_implementation() == 'PyPy':
        # Skip for PyPy...
        return

    # file exists, with same contents
    # read

    write_randomness()

    f = open(fname, "r")
    _f = dill.loads(dill.dumps(f, fmode=fmode))#, strictio=strictio))
    assert _f.mode == f.mode
    assert _f.tell() == f.tell()
    assert _f.read() == f.read()
    f.close()
    _f.close()

    # write

    f = open(fname, "w")
    f.write("hello")
    f_dumped = dill.dumps(f, fmode=fmode)#, strictio=strictio)
    f1mode = f.mode
    ftell = f.tell()
    f.close()
    f2 = dill.loads(f_dumped) #FIXME: fails due to pypy/issues/1233
    # TypeError: expected py_object instance instead of str
    f2mode = f2.mode
    f2tell = f2.tell()
    f2name = f2.name
    f2.write(" world!")
    f2.close()

    if fmode == dill.HANDLE_FMODE:
        assert open(fname).read() == " world!"
        assert f2mode == f1mode
        assert f2tell == 0
    elif fmode == dill.CONTENTS_FMODE:
        assert open(fname).read() == "hello world!"
        assert f2mode == f1mode
        assert f2tell == ftell
        assert f2name == fname
    elif fmode == dill.FILE_FMODE:
        assert open(fname).read() == "hello world!"
        assert f2mode == f1mode
        assert f2tell == ftell
    else:
        raise RuntimeError("Unknown file mode '%s'" % fmode)

    # append

    trunc_file()

    f = open(fname, "a")
    f.write("hello")
    f_dumped = dill.dumps(f, fmode=fmode)#, strictio=strictio)
    f1mode = f.mode
    ftell = f.tell()
    f.close()
    f2 = dill.loads(f_dumped)
    f2mode = f2.mode
    f2tell = f2.tell()
    f2.write(" world!")
    f2.close()

    assert f2mode == f1mode
    if fmode == dill.CONTENTS_FMODE:
        assert open(fname).read() == "hello world!"
        assert f2tell == ftell
    elif fmode == dill.HANDLE_FMODE:
        assert open(fname).read() == "hello world!"
        assert f2tell == ftell
    elif fmode == dill.FILE_FMODE:
        assert open(fname).read() == "hello world!"
        assert f2tell == ftell
    else:
        raise RuntimeError("Unknown file mode '%s'" % fmode)

    # file exists, with different contents (smaller size)
    # read

    write_randomness()

    f = open(fname, "r")
    fstr = f.read()
    f_dumped = dill.dumps(f, fmode=fmode)#, strictio=strictio)
    f1mode = f.mode
    ftell = f.tell()
    f.close()
    _flen = 150
    _fstr = write_randomness(number=_flen)

    if strictio:  # throw error if ftell > EOF
        assert throws(dill.loads, (f_dumped,), buffer_error)
    else:
        f2 = dill.loads(f_dumped)
        assert f2.mode == f1mode
        if fmode == dill.CONTENTS_FMODE:
            assert f2.tell() == _flen
            assert f2.read() == ""
            f2.seek(0)
            assert f2.read() == _fstr
            assert f2.tell() == _flen  # 150
        elif fmode == dill.HANDLE_FMODE:
            assert f2.tell() == 0
            assert f2.read() == _fstr
            assert f2.tell() == _flen  # 150
        elif fmode == dill.FILE_FMODE:
            assert f2.tell() == ftell  # 200
            assert f2.read() == ""
            f2.seek(0)
            assert f2.read() == fstr
            assert f2.tell() == ftell  # 200
        else:
            raise RuntimeError("Unknown file mode '%s'" % fmode)
        f2.close()

    # write

    write_randomness()

    f = open(fname, "w")
    f.write("hello")
    f_dumped = dill.dumps(f, fmode=fmode)#, strictio=strictio)
    f1mode = f.mode
    ftell = f.tell()
    f.close()
    fstr = open(fname).read()

    f = open(fname, "w")
    f.write("h")
    _ftell = f.tell()
    f.close()

    if strictio:  # throw error if ftell > EOF
        assert throws(dill.loads, (f_dumped,), buffer_error)
    else:
        f2 = dill.loads(f_dumped)
        f2mode = f2.mode
        f2tell = f2.tell()
        f2.write(" world!")
        f2.close()
        if fmode == dill.CONTENTS_FMODE:
            assert open(fname).read() == "h world!"
            assert f2mode == f1mode
            assert f2tell == _ftell
        elif fmode == dill.HANDLE_FMODE:
            assert open(fname).read() == " world!"
            assert f2mode == f1mode
            assert f2tell == 0
        elif fmode == dill.FILE_FMODE:
            assert open(fname).read() == "hello world!"
            assert f2mode == f1mode
            assert f2tell == ftell
        else:
            raise RuntimeError("Unknown file mode '%s'" % fmode)
        f2.close()

    # append

    trunc_file()

    f = open(fname, "a")
    f.write("hello")
    f_dumped = dill.dumps(f, fmode=fmode)#, strictio=strictio)
    f1mode = f.mode
    ftell = f.tell()
    f.close()
    fstr = open(fname).read()

    f = open(fname, "w")
    f.write("h")
    _ftell = f.tell()
    f.close()

    if strictio:  # throw error if ftell > EOF
        assert throws(dill.loads, (f_dumped,), buffer_error)
    else:
        f2 = dill.loads(f_dumped)
        f2mode = f2.mode
        f2tell = f2.tell()
        f2.write(" world!")
        f2.close()
        assert f2mode == f1mode
        if fmode == dill.CONTENTS_FMODE:
            # position of writes cannot be changed on some OSs
            assert open(fname).read() == "h world!"
            assert f2tell == _ftell
        elif fmode == dill.HANDLE_FMODE:
            assert open(fname).read() == "h world!"
            assert f2tell == _ftell
        elif fmode == dill.FILE_FMODE:
            assert open(fname).read() == "hello world!"
            assert f2tell == ftell
        else:
            raise RuntimeError("Unknown file mode '%s'" % fmode)
        f2.close()

    # file does not exist
    # read

    write_randomness()

    f = open(fname, "r")
    fstr = f.read()
    f_dumped = dill.dumps(f, fmode=fmode)#, strictio=strictio)
    f1mode = f.mode
    ftell = f.tell()
    f.close()

    os.remove(fname)

    if strictio:  # throw error if file DNE
        assert throws(dill.loads, (f_dumped,), dne_error)
    else:
        f2 = dill.loads(f_dumped)
        assert f2.mode == f1mode
        if fmode == dill.CONTENTS_FMODE:
            # FIXME: this fails on systems where f2.tell() always returns 0
            # assert f2.tell() == ftell # 200
            assert f2.read() == ""
            f2.seek(0)
            assert f2.read() == ""
            assert f2.tell() == 0
        elif fmode == dill.FILE_FMODE:
            assert f2.tell() == ftell  # 200
            assert f2.read() == ""
            f2.seek(0)
            assert f2.read() == fstr
            assert f2.tell() == ftell  # 200
        elif fmode == dill.HANDLE_FMODE:
            assert f2.tell() == 0
            assert f2.read() == ""
            assert f2.tell() == 0
        else:
            raise RuntimeError("Unknown file mode '%s'" % fmode)
        f2.close()

    # write

    write_randomness()

    f = open(fname, "w+")
    f.write("hello")
    f_dumped = dill.dumps(f, fmode=fmode)#, strictio=strictio)
    ftell = f.tell()
    f1mode = f.mode
    f.close()

    os.remove(fname)

    if strictio:  # throw error if file DNE
        assert throws(dill.loads, (f_dumped,), dne_error)
    else:
        f2 = dill.loads(f_dumped)
        f2mode = f2.mode
        f2tell = f2.tell()
        f2.write(" world!")
        f2.close()
        if fmode == dill.CONTENTS_FMODE:
            assert open(fname).read() == " world!"
            assert f2mode == 'w+'
            assert f2tell == 0
        elif fmode == dill.HANDLE_FMODE:
            assert open(fname).read() == " world!"
            assert f2mode == f1mode
            assert f2tell == 0
        elif fmode == dill.FILE_FMODE:
            assert open(fname).read() == "hello world!"
            assert f2mode == f1mode
            assert f2tell == ftell
        else:
            raise RuntimeError("Unknown file mode '%s'" % fmode)

    # append

    trunc_file()

    f = open(fname, "a")
    f.write("hello")
    f_dumped = dill.dumps(f, fmode=fmode)#, strictio=strictio)
    ftell = f.tell()
    f1mode = f.mode
    f.close()

    os.remove(fname)

    if strictio:  # throw error if file DNE
        assert throws(dill.loads, (f_dumped,), dne_error)
    else:
        f2 = dill.loads(f_dumped)
        f2mode = f2.mode
        f2tell = f2.tell()
        f2.write(" world!")
        f2.close()
        assert f2mode == f1mode
        if fmode == dill.CONTENTS_FMODE:
            assert open(fname).read() == " world!"
            assert f2tell == 0
        elif fmode == dill.HANDLE_FMODE:
            assert open(fname).read() == " world!"
            assert f2tell == 0
        elif fmode == dill.FILE_FMODE:
            assert open(fname).read() == "hello world!"
            assert f2tell == ftell
        else:
            raise RuntimeError("Unknown file mode '%s'" % fmode)

    # file exists, with different contents (larger size)
    # read

    write_randomness()

    f = open(fname, "r")
    fstr = f.read()
    f_dumped = dill.dumps(f, fmode=fmode)#, strictio=strictio)
    f1mode = f.mode
    ftell = f.tell()
    f.close()
    _flen = 250
    _fstr = write_randomness(number=_flen)

    # XXX: no safe_file: no way to be 'safe'?

    f2 = dill.loads(f_dumped)
    assert f2.mode == f1mode
    if fmode == dill.CONTENTS_FMODE:
        assert f2.tell() == ftell  # 200
        assert f2.read() == _fstr[ftell:]
        f2.seek(0)
        assert f2.read() == _fstr
        assert f2.tell() == _flen  # 250
    elif fmode == dill.HANDLE_FMODE:
        assert f2.tell() == 0
        assert f2.read() == _fstr
        assert f2.tell() == _flen  # 250
    elif fmode == dill.FILE_FMODE:
        assert f2.tell() == ftell  # 200
        assert f2.read() == ""
        f2.seek(0)
        assert f2.read() == fstr
        assert f2.tell() == ftell  # 200
    else:
        raise RuntimeError("Unknown file mode '%s'" % fmode)
    f2.close()  # XXX: other alternatives?

    # write

    f = open(fname, "w")
    f.write("hello")
    f_dumped = dill.dumps(f, fmode=fmode)#, strictio=strictio)
    f1mode = f.mode
    ftell = f.tell()

    fstr = open(fname).read()

    f.write(" and goodbye!")
    _ftell = f.tell()
    f.close()

    # XXX: no safe_file: no way to be 'safe'?

    f2 = dill.loads(f_dumped)
    f2mode = f2.mode
    f2tell = f2.tell()
    f2.write(" world!")
    f2.close()
    if fmode == dill.CONTENTS_FMODE:
        assert open(fname).read() == "hello world!odbye!"
        assert f2mode == f1mode
        assert f2tell == ftell
    elif fmode == dill.HANDLE_FMODE:
        assert open(fname).read() == " world!"
        assert f2mode == f1mode
        assert f2tell == 0
    elif fmode == dill.FILE_FMODE:
        assert open(fname).read() == "hello world!"
        assert f2mode == f1mode
        assert f2tell == ftell
    else:
        raise RuntimeError("Unknown file mode '%s'" % fmode)
    f2.close()

    # append

    trunc_file()

    f = open(fname, "a")
    f.write("hello")
    f_dumped = dill.dumps(f, fmode=fmode)#, strictio=strictio)
    f1mode = f.mode
    ftell = f.tell()
    fstr = open(fname).read()

    f.write(" and goodbye!")
    _ftell = f.tell()
    f.close()

    # XXX: no safe_file: no way to be 'safe'?

    f2 = dill.loads(f_dumped)
    f2mode = f2.mode
    f2tell = f2.tell()
    f2.write(" world!")
    f2.close()
    assert f2mode == f1mode
    if fmode == dill.CONTENTS_FMODE:
        assert open(fname).read() == "hello and goodbye! world!"
        assert f2tell == ftell
    elif fmode == dill.HANDLE_FMODE:
        assert open(fname).read() == "hello and goodbye! world!"
        assert f2tell == _ftell
    elif fmode == dill.FILE_FMODE:
        assert open(fname).read() == "hello world!"
        assert f2tell == ftell
    else:
        raise RuntimeError("Unknown file mode '%s'" % fmode)
    f2.close()

