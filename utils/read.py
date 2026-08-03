import copy
import os
import sys

def read(fp, as_version=nbformat.NO_CONVERT, fmt=None, config=None, **kwargs):
    """Read a notebook from a file name or a file object

    :param fp: a file name or a file object
    :param as_version: see nbformat.read
    :param fmt: (optional) the jupytext format like `md`, `py:percent`, ...
    :param config: (optional) a Jupytext configuration object
    :param kwargs: (not used) additional parameters for nbformat.read
    :return: the notebook
    """
    if as_version != nbformat.NO_CONVERT and not isinstance(as_version, int):
        raise TypeError("Second argument 'as_version' should be either nbformat.NO_CONVERT, or an integer.")

    if fp == "-":
        text = sys.stdin.read()
        # Update the input format by reference if missing
        if isinstance(fmt, dict) and not fmt:
            fmt.update(long_form_one_format(divine_format(text)))
        return reads(text, fmt)

    if not hasattr(fp, "read"):
        # Treat fp as a file name
        fp = str(fp)
        _, ext = os.path.splitext(fp)
        fmt = copy(fmt or {})
        if not isinstance(fmt, dict):
            fmt = long_form_one_format(fmt)
        fmt.update({"extension": ext})
        with open(fp, encoding="utf-8") as stream:
            return read(stream, as_version=as_version, fmt=fmt, config=config, **kwargs)

    if fmt is not None:
        fmt = long_form_one_format(fmt)
        if fmt["extension"] == ".ipynb":
            notebook = nbformat.read(fp, as_version, **kwargs)
            rearrange_jupytext_metadata(notebook.metadata)
            return notebook

    return reads(fp.read(), fmt, config=config, **kwargs)


def read(fp, format="DEPRECATED", **kwargs):
    """Read a notebook from a file and return the NotebookNode object.

    This function properly handles notebooks of any version. The notebook
    returned will always be in the current version's format.

    Parameters
    ----------
    fp : file
        Any file-like object with a read method.

    Returns
    -------
    nb : NotebookNode
        The notebook that was read.
    """
    return reads(fp.read(), **kwargs)


def read(fp, **kwargs):
    """Read a notebook from a file and return the NotebookNode object.

    This function properly reads notebooks of any version.  No version
    conversion is performed.

    Parameters
    ----------
    fp : file
        Any file-like object with a read method.

    Returns
    -------
    nb : NotebookNode
        The notebook that was read.
    """
    return reads(fp.read(), **kwargs)


def read(fp, as_version, capture_validation_error=None, **kwargs):
    """Read a notebook from a file as a NotebookNode of the given version.

    The string can contain a notebook of any version.
    The notebook will be returned `as_version`, converting, if necessary.

    Notebook format errors will be logged.

    Parameters
    ----------
    fp : file or str
        A file-like object with a read method that returns unicode (use
        ``io.open()`` in Python 2), or a path to a file.
    as_version : int
        The version of the notebook format to return.
        The notebook will be converted, if necessary.
        Pass nbformat.NO_CONVERT to prevent conversion.
    capture_validation_error : dict, optional
        If provided, a key of "ValidationError" with a
        value of the ValidationError instance will be added
        to the dictionary.

    Returns
    -------
    nb : NotebookNode
        The notebook that was read.
    """

    try:
        buf = fp.read()
    except AttributeError:
        with open(fp, encoding="utf8") as f:  # noqa: PTH123
            return reads(f.read(), as_version, capture_validation_error, **kwargs)

    return reads(buf, as_version, capture_validation_error, **kwargs)


def read(filename, mmap=False):
    """
    Open a WAV file.

    Return the sample rate (in samples/sec) and data from an LPCM WAV file.

    Parameters
    ----------
    filename : str or open file handle
        Input WAV file.
    mmap : bool, optional
        Whether to read data as memory-mapped (default: False).  Not compatible
        with some bit depths; see Notes.  Only to be used on real files.

        .. versionadded:: 0.12.0

    Returns
    -------
    rate : int
        Sample rate of WAV file.
    data : numpy array
        Data read from WAV file. Data-type is determined from the file;
        see Notes.  Data is 1-D for 1-channel WAV, or 2-D of shape
        (Nsamples, Nchannels) otherwise. If a file-like input without a
        C-like file descriptor (e.g., :class:`python:io.BytesIO`) is
        passed, this will not be writeable.

    Notes
    -----
    Common data types: [1]_

    =====================  ===========  ===========  =============
         WAV format            Min          Max       NumPy dtype
    =====================  ===========  ===========  =============
    32-bit floating-point  -1.0         +1.0         float32
    32-bit integer PCM     -2147483648  +2147483647  int32
    24-bit integer PCM     -2147483648  +2147483392  int32
    16-bit integer PCM     -32768       +32767       int16
    8-bit integer PCM      0            255          uint8
    =====================  ===========  ===========  =============

    WAV files can specify arbitrary bit depth, and this function supports
    reading any integer PCM depth from 1 to 64 bits.  Data is returned in the
    smallest compatible numpy int type, in left-justified format.  8-bit and
    lower is unsigned, while 9-bit and higher is signed.

    For example, 24-bit data will be stored as int32, with the MSB of the
    24-bit data stored at the MSB of the int32, and typically the least
    significant byte is 0x00.  (However, if a file actually contains data past
    its specified bit depth, those bits will be read and output, too. [2]_)

    This bit justification and sign matches WAV's native internal format, which
    allows memory mapping of WAV files that use 1, 2, 4, or 8 bytes per sample
    (so 24-bit files cannot be memory-mapped, but 32-bit can).

    IEEE float PCM in 32- or 64-bit format is supported, with or without mmap.
    Values exceeding [-1, +1] are not clipped.

    Non-linear PCM (mu-law, A-law) is not supported.

    References
    ----------
    .. [1] IBM Corporation and Microsoft Corporation, "Multimedia Programming
       Interface and Data Specifications 1.0", section "Data Format of the
       Samples", August 1991
       http://www.tactilemedia.com/info/MCI_Control_Info.html
    .. [2] Adobe Systems Incorporated, "Adobe Audition 3 User Guide", section
       "Audio file formats: 24-bit Packed Int (type 1, 20-bit)", 2007

    Examples
    --------
    >>> from os.path import dirname, join as pjoin
    >>> from scipy.io import wavfile
    >>> import scipy.io

    Get the filename for an example .wav file from the tests/data directory.

    >>> data_dir = pjoin(dirname(scipy.io.__file__), 'tests', 'data')
    >>> wav_fname = pjoin(data_dir, 'test-44100Hz-2ch-32bit-float-be.wav')

    Load the .wav file contents.

    >>> samplerate, data = wavfile.read(wav_fname)
    >>> print(f"number of channels = {data.shape[1]}")
    number of channels = 2
    >>> length = data.shape[0] / samplerate
    >>> print(f"length = {length}s")
    length = 0.01s

    Plot the waveform.

    >>> import matplotlib.pyplot as plt
    >>> import numpy as np
    >>> time = np.linspace(0., length, data.shape[0])
    >>> plt.plot(time, data[:, 0], label="Left channel")
    >>> plt.plot(time, data[:, 1], label="Right channel")
    >>> plt.legend()
    >>> plt.xlabel("Time [s]")
    >>> plt.ylabel("Amplitude")
    >>> plt.show()

    """
    if hasattr(filename, 'read'):
        fid = filename
        mmap = False
    else:
        fid = open(filename, 'rb')
    
    if not (was_seekable := fid.seekable()):
        fid = SeekEmulatingReader(fid)

    try:
        file_size, is_big_endian, is_rf64, rf64_chunk_size = _read_riff_chunk(fid)
        fmt_chunk_received = False
        data_chunk_received = False
        while fid.tell() < file_size:
            # read the next chunk
            chunk_id = fid.read(4)

            if not chunk_id:
                if data_chunk_received:
                    # End of file but data successfully read
                    warnings.warn(
                        f"Reached EOF prematurely; finished at {fid.tell():d} bytes, "
                        f"expected {file_size:d} bytes from header.",
                        WavFileWarning, stacklevel=2)
                    break
                else:
                    raise ValueError("Unexpected end of file.")
            elif len(chunk_id) < 4:
                msg = f"Incomplete chunk ID: {repr(chunk_id)}"
                # If we have the data, ignore the broken chunk
                if fmt_chunk_received and data_chunk_received:
                    warnings.warn(msg + ", ignoring it.", WavFileWarning,
                                  stacklevel=2)
                else:
                    raise ValueError(msg)

            if chunk_id == b'fmt ':
                fmt_chunk_received = True
                fmt_chunk = _read_fmt_chunk(fid, is_big_endian)
                format_tag, channels, fs = fmt_chunk[1:4]
                bit_depth = fmt_chunk[6]
                block_align = fmt_chunk[5]
            elif chunk_id == b'fact':
                _skip_unknown_chunk(fid, is_big_endian)
            elif chunk_id == b'data':
                data_chunk_received = True
                if not fmt_chunk_received:
                    raise ValueError("No fmt chunk before data")
                data = _read_data_chunk(fid, format_tag, channels, bit_depth,
                                        is_big_endian, is_rf64, block_align,
                                        mmap, rf64_chunk_size)
            elif chunk_id == b'LIST':
                # Someday this could be handled properly but for now skip it
                _skip_unknown_chunk(fid, is_big_endian)
            elif chunk_id in {b'JUNK', b'Fake'}:
                # Skip alignment chunks without warning
                _skip_unknown_chunk(fid, is_big_endian)
            else:
                warnings.warn("Chunk (non-data) not understood, skipping it.",
                              WavFileWarning, stacklevel=2)
                _skip_unknown_chunk(fid, is_big_endian)
    finally:
        if not hasattr(filename, 'read'):
            fid.close()
        elif was_seekable:
            # Rewind, if we are able, so that caller can do something
            # else with the raw WAV stream.
            fid.seek(0)

    return fs, data


def read(fp, **kwargs):
    """REMOVED"""
    raise Exception(REMOVED_MSG)


def read(path, onlyHeader=False):
    """reads any Type 1 font file, returns raw data"""
    _, ext = os.path.splitext(path)
    ext = ext.lower()
    creator, typ = getMacCreatorAndType(path)
    if typ == "LWFN":
        return readLWFN(path, onlyHeader), "LWFN"
    if ext == ".pfb":
        return readPFB(path, onlyHeader), "PFB"
    else:
        return readOther(path), "OTHER"

