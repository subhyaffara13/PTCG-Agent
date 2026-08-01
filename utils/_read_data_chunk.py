
def _read_data_chunk(fid, format_tag, channels, bit_depth, is_big_endian, is_rf64,
                     block_align, mmap=False, rf64_chunk_size=None):
    """
    Notes
    -----
    Assumes file pointer is immediately after the 'data' id

    It's possible to not use all available bits in a container, or to store
    samples in a container bigger than necessary, so bytes_per_sample uses
    the actual reported container size (nBlockAlign / nChannels).  Real-world
    examples:

    Adobe Audition's "24-bit packed int (type 1, 20-bit)"

        nChannels = 2, nBlockAlign = 6, wBitsPerSample = 20

    http://www-mmsp.ece.mcgill.ca/Documents/AudioFormats/WAVE/Samples/AFsp/M1F1-int12-AFsp.wav
    is:

        nChannels = 2, nBlockAlign = 4, wBitsPerSample = 12

    http://www-mmsp.ece.mcgill.ca/Documents/AudioFormats/WAVE/Docs/multichaudP.pdf
    gives an example of:

        nChannels = 2, nBlockAlign = 8, wBitsPerSample = 20
    """
    if is_big_endian:
        fmt = '>'
    else:
        fmt = '<'

    # Size of the data subchunk in bytes
    if not is_rf64:
        size = struct.unpack(fmt+'I', fid.read(4))[0]
    else:
        # chunk size is stored in global file header for RF64
        size = rf64_chunk_size
        # skip data chunk size as it is 0xFFFFFFF
        fid.read(4)

    # Number of bytes per sample (sample container size)
    bytes_per_sample = block_align // channels
    n_samples = size // bytes_per_sample

    if format_tag == WAVE_FORMAT.PCM:
        if 1 <= bit_depth <= 8:
            dtype = 'u1'  # WAV of 8-bit integer or less are unsigned
        elif bytes_per_sample in {3, 5, 6, 7}:
            # No compatible dtype.  Load as raw bytes for reshaping later.
            dtype = 'V1'
        elif bit_depth <= 64:
            # Remaining bit depths can map directly to signed numpy dtypes
            dtype = f'{fmt}i{bytes_per_sample}'
        else:
            raise ValueError("Unsupported bit depth: the WAV file "
                             f"has {bit_depth}-bit integer data.")
    elif format_tag == WAVE_FORMAT.IEEE_FLOAT:
        if bit_depth in {32, 64}:
            dtype = f'{fmt}f{bytes_per_sample}'
        else:
            raise ValueError("Unsupported bit depth: the WAV file "
                             f"has {bit_depth}-bit floating-point data.")
    else:
        _raise_bad_format(format_tag)

    start = fid.tell()
    if not mmap:
        try:
            count = size if dtype == 'V1' else n_samples
            data = np.fromfile(fid, dtype=dtype, count=count)
        except io.UnsupportedOperation:  # not a C-like file
            fid.seek(start, 0)  # just in case it seeked, though it shouldn't
            data = np.frombuffer(fid.read(size), dtype=dtype)

        if dtype == 'V1':
            # Rearrange raw bytes into smallest compatible numpy dtype
            dt = f'{fmt}i4' if bytes_per_sample == 3 else f'{fmt}i8'
            a = np.zeros((len(data) // bytes_per_sample, np.dtype(dt).itemsize),
                            dtype='V1')
            if is_big_endian:
                a[:, :bytes_per_sample] = data.reshape((-1, bytes_per_sample))
            else:
                a[:, -bytes_per_sample:] = data.reshape((-1, bytes_per_sample))
            data = a.view(dt).reshape(a.shape[:-1])
    else:
        if bytes_per_sample in {1, 2, 4, 8}:
            start = fid.tell()
            data = np.memmap(fid, dtype=dtype, mode='c', offset=start,
                                shape=(n_samples,))
            fid.seek(start + size)
        else:
            raise ValueError("mmap=True not compatible with "
                             f"{bytes_per_sample}-byte container size.")

    _handle_pad_byte(fid, size)

    if channels > 1:
        data = data.reshape(-1, channels)
    return data

