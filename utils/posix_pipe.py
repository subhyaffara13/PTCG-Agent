
def posix_pipe(fin, fout, delim=b'\\n', buf_size=256,
               callback=lambda float: None, callback_len=True):
    """
    Params
    ------
    fin  : binary file with `read(buf_size : int)` method
    fout  : binary file with `write` (and optionally `flush`) methods.
    callback  : function(float), e.g.: `tqdm.update`
    callback_len  : If (default: True) do `callback(len(buffer))`.
      Otherwise, do `callback(data) for data in buffer.split(delim)`.
    """
    fp_write = fout.write

    if not delim:
        while True:
            tmp = fin.read(buf_size)

            # flush at EOF
            if not tmp:
                getattr(fout, 'flush', lambda: None)()
                return

            fp_write(tmp)
            callback(len(tmp))
        # return

    buf = b''
    len_delim = len(delim)
    # n = 0
    while True:
        tmp = fin.read(buf_size)

        # flush at EOF
        if not tmp:
            if buf:
                fp_write(buf)
                if callback_len:
                    # n += 1 + buf.count(delim)
                    callback(1 + buf.count(delim))
                else:
                    for i in buf.split(delim):
                        callback(i)
            getattr(fout, 'flush', lambda: None)()
            return  # n

        while True:
            i = tmp.find(delim)
            if i < 0:
                buf += tmp
                break
            fp_write(buf + tmp[:i + len(delim)])
            # n += 1
            callback(1 if callback_len else (buf + tmp[:i]))
            buf = b''
            tmp = tmp[i + len_delim:]

