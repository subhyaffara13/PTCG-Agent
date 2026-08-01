
def copychunked(src, dest):
    chunksize = 524288  # half a meg of bytes
    fsrc = src.open("rb")
    try:
        fdest = dest.open("wb")
        try:
            while 1:
                buf = fsrc.read(chunksize)
                if not buf:
                    break
                fdest.write(buf)
        finally:
            fdest.close()
    finally:
        fsrc.close()

