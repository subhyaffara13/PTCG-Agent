
def _write_pyc_fp(
    fp: IO[bytes], source_stat: os.stat_result, co: types.CodeType
) -> None:
    # Technically, we don't have to have the same pyc format as
    # (C)Python, since these "pycs" should never be seen by builtin
    # import. However, there's little reason to deviate.
    fp.write(importlib.util.MAGIC_NUMBER)
    # https://www.python.org/dev/peps/pep-0552/
    flags = b"\x00\x00\x00\x00"
    fp.write(flags)
    # as of now, bytecode header expects 32-bit numbers for size and mtime (#4903)
    mtime = int(source_stat.st_mtime) & 0xFFFFFFFF
    size = source_stat.st_size & 0xFFFFFFFF
    # "<LL" stands for 2 unsigned longs, little-endian.
    fp.write(struct.pack("<LL", mtime, size))
    fp.write(marshal.dumps(co))

