
def _get_matfile_version(fileobj):
    # Mat4 files have a zero somewhere in first 4 bytes
    fileobj.seek(0)
    hdr_bytes = fileobj.read(_HDR_N_BYTES)
    if len(hdr_bytes) < _HDR_N_BYTES:
        raise MatReadError("Mat file appears to be truncated")
    if hdr_bytes.count(0) == _HDR_N_BYTES:
        raise MatReadError("Mat file appears to be corrupt "
                           f"(first {_HDR_N_BYTES} bytes == 0)")
    mopt_ints = np.ndarray(shape=(4,), dtype=np.uint8, buffer=hdr_bytes[:4])
    if 0 in mopt_ints:
        fileobj.seek(0)
        return (0,0)
    # For 5 format or 7.3 format we need to read an integer in the
    # header. Bytes 124 through 128 contain a version integer and an
    # endian test string
    fileobj.seek(124)
    tst_str = fileobj.read(4)
    fileobj.seek(0)
    maj_ind = int(tst_str[2] == b'I'[0])
    maj_val = int(tst_str[maj_ind])
    min_val = int(tst_str[1 - maj_ind])
    ret = (maj_val, min_val)
    if maj_val in (1, 2):
        return ret
    raise ValueError('Unknown mat file type, version {}, {}'.format(*ret))

