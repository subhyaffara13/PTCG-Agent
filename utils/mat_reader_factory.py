
def mat_reader_factory(file_name, appendmat=True, **kwargs):
    """
    Create reader for matlab .mat format files.

    Returns
    -------
    matreader : MatFileReader object
       Initialized instance of MatFileReader class matching the mat file
       type detected in `filename`.
    file_opened : bool
       Whether the file was opened by this routine.

    """
    byte_stream, file_opened = _open_file(file_name, appendmat)
    mjv, mnv = _get_matfile_version(byte_stream)
    if mjv == 0:
        return MatFile4Reader(byte_stream, **kwargs), file_opened
    elif mjv == 1:
        return MatFile5Reader(byte_stream, **kwargs), file_opened
    elif mjv == 2:
        raise NotImplementedError('Please use HDF reader for matlab v7.3 '
                                  'files, e.g. h5py')
    else:
        raise TypeError(f'Did not recognize version {mjv}')

