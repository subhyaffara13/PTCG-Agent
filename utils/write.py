import copy
import os
import sys
from pathlib import Path


def Write(packer_type, buf, head, n):
  """Write encodes `n` at buf[head] using `packer_type`."""
  packer_type.pack_into(buf, head, n)


def write(nb, fp, version=nbformat.NO_CONVERT, fmt=None, config=None, **kwargs):
    """Write a notebook to a file name or a file object

    :param nb: the notebook
    :param fp: a file name or a file object
    :param version: see nbformat.write
    :param fmt: (optional if fp is a file name) the jupytext format like `md`, `py:percent`, ...
    :param config: (optional) a Jupytext configuration object
    :param kwargs: (not used) additional parameters for nbformat.write
    """
    if fp == "-":
        # Use sys.stdout.buffer when possible, and explicit utf-8 encoding, cf. #331
        content = writes(nb, version=version, fmt=fmt, config=config, **kwargs)
        try:
            # Python 3
            sys.stdout.buffer.write(content.encode("utf-8"))
        except AttributeError:
            sys.stdout.write(content.encode("utf-8"))
        return

    if not hasattr(fp, "write"):
        # Treat fp as a file name
        fp = str(fp)
        _, ext = os.path.splitext(fp)
        fmt = copy(fmt or {})
        fmt = long_form_one_format(fmt, update={"extension": ext})
        create_prefix_dir(fp, fmt, None)

        with open(fp, "w", encoding="utf-8") as stream:
            write(nb, stream, version=version, fmt=fmt, config=config, **kwargs)
            return
    else:
        assert fmt is not None, "'fmt' argument in jupytext.write is mandatory unless fp is a file name"

    content = writes(nb, version=version, fmt=fmt, config=config, **kwargs)
    if isinstance(content, bytes):
        content = content.decode("utf8")
    fp.write(content)
    if not content.endswith("\n"):
        fp.write("\n")


def write(nb, fp, format="DEPRECATED", **kwargs):
    """Write a notebook to a file in a given format in the current nbformat version.

    This function always writes the notebook in the current nbformat version.

    Parameters
    ----------
    nb : NotebookNode
        The notebook to write.
    fp : file
        Any file-like object with a write method.
    """
    s = writes(nb, **kwargs)
    if isinstance(s, bytes):
        s = s.decode("utf8")
    return fp.write(s)


def write(nb, fp, version=NO_CONVERT, capture_validation_error=None, **kwargs):
    """Write a notebook to a file in a given nbformat version.

    The file-like object must accept unicode input.

    Parameters
    ----------
    nb : NotebookNode
        The notebook to write.
    fp : file or str
        Any file-like object with a write method that accepts unicode, or
        a path to write a file.
    version : int, optional
        The nbformat version to write.
        If nb is not this version, it will be converted.
        If unspecified, or specified as nbformat.NO_CONVERT,
        the notebook's own version will be used and no conversion performed.
    capture_validation_error : dict, optional
        If provided, a key of "ValidationError" with a
        value of the ValidationError instance will be added
        to the dictionary.
    """
    s = writes(nb, version, capture_validation_error, **kwargs)
    if isinstance(s, bytes):
        s = s.decode("utf8")

    try:
        fp.write(s)
        if not s.endswith("\n"):
            fp.write("\n")
    except AttributeError:
        with Path(fp).open("w", encoding="utf8") as f:
            f.write(s)
            if not s.endswith("\n"):
                f.write("\n")


def write(
    content: str | bytes,
    extension: str,
    extra: str = "",
    hash_type: str = "code",
    specified_dir: str = "",
    key: str | None = None,
) -> tuple[str, str]:
    if key is None:
        # use striped content to compute hash so we don't end up with different
        # hashes just because the content begins/ends with different number of
        # spaces.
        key = get_hash(content.strip(), extra, hash_type)
    basename, _subdir, path = get_path(key, extension, specified_dir)
    if not os.path.exists(path):
        write_atomic(path, content, make_dirs=True)
    return basename, path


def write(filename, rate, data):
    """
    Write a NumPy array as a WAV file.

    Parameters
    ----------
    filename : str or open file handle
        Output wav file.
    rate : int
        The sample rate (in samples/sec).
    data : ndarray
        A 1-D or 2-D NumPy array of either integer or float data-type.

    Notes
    -----
    * Writes a simple uncompressed WAV file.
    * To write multiple-channels, use a 2-D array of shape
      (Nsamples, Nchannels).
    * The bits-per-sample and PCM/float will be determined by the data-type.

    Common data types: [1]_

    =====================  ===========  ===========  =============
         WAV format            Min          Max       NumPy dtype
    =====================  ===========  ===========  =============
    32-bit floating-point  -1.0         +1.0         float32
    32-bit PCM             -2147483648  +2147483647  int32
    16-bit PCM             -32768       +32767       int16
    8-bit PCM              0            255          uint8
    =====================  ===========  ===========  =============

    Note that 8-bit PCM is unsigned.

    References
    ----------
    .. [1] IBM Corporation and Microsoft Corporation, "Multimedia Programming
       Interface and Data Specifications 1.0", section "Data Format of the
       Samples", August 1991
       http://www.tactilemedia.com/info/MCI_Control_Info.html

    Examples
    --------
    Create a 100Hz sine wave, sampled at 44100Hz.
    Write to 16-bit PCM, Mono.

    >>> from scipy.io.wavfile import write
    >>> import numpy as np
    >>> samplerate = 44100; fs = 100
    >>> t = np.linspace(0., 1., samplerate)
    >>> amplitude = np.iinfo(np.int16).max
    >>> data = amplitude * np.sin(2. * np.pi * fs * t)
    >>> write("example.wav", samplerate, data.astype(np.int16))

    """
    if hasattr(filename, 'write'):
        fid = filename
    else:
        fid = open(filename, 'wb')

    fs = rate

    try:
        dkind = data.dtype.kind
        allowed_dtypes = ['float32', 'float64',
                          'uint8', 'int16', 'int32', 'int64']
        if data.dtype.name not in allowed_dtypes:
            raise ValueError(f"Unsupported data type '{data.dtype}'")

        header_data = b''

        header_data += b'RIFF'
        header_data += b'\x00\x00\x00\x00'
        header_data += b'WAVE'

        # fmt chunk
        header_data += b'fmt '
        if dkind == 'f':
            format_tag = WAVE_FORMAT.IEEE_FLOAT
        else:
            format_tag = WAVE_FORMAT.PCM
        if data.ndim == 1:
            channels = 1
        else:
            channels = data.shape[1]
        bit_depth = data.dtype.itemsize * 8
        bytes_per_second = fs*(bit_depth // 8)*channels
        block_align = channels * (bit_depth // 8)

        fmt_chunk_data = struct.pack('<HHIIHH', format_tag, channels, fs,
                                     bytes_per_second, block_align, bit_depth)
        if not (dkind == 'i' or dkind == 'u'):
            # add cbSize field for non-PCM files
            fmt_chunk_data += b'\x00\x00'

        header_data += struct.pack('<I', len(fmt_chunk_data))
        header_data += fmt_chunk_data

        # check data size (needs to be immediately before the data chunk)
        # if too large for standard RIFF, use RF64 instead
        resulting_file_size = len(header_data) + 4 + 4 + data.nbytes
        is_rf64 = (resulting_file_size - 8) > 0xFFFFFFFF
        if is_rf64:
            header_data = b''
            header_data += b'RF64'
            header_data += b'\xFF\xFF\xFF\xFF'
            header_data += b'WAVE'
            header_data += b'ds64'
            # size of ds64 chunk
            header_data += struct.pack('<I', 28)
            # will be filled later with real file size
            header_data += struct.pack('<Q', 0)
            header_data += struct.pack('<Q', data.nbytes)
            header_data += struct.pack('<Q', data.shape[0])
            # ignore 'table' field for now
            header_data += struct.pack('<I', 0)
            header_data += b'fmt '
            header_data += struct.pack('<I', len(fmt_chunk_data))
            header_data += fmt_chunk_data

        # fact chunk (non-PCM files)
        if not (dkind == 'i' or dkind == 'u'):
            header_data += b'fact'
            header_data += struct.pack('<II', 4, data.shape[0])

        fid.write(header_data)

        # data chunk
        fid.write(b'data')
        # write data chunk size, unless its too big in which case 0xFFFFFFFF is written
        fid.write(struct.pack('<I', min(data.nbytes, 4294967295)))

        if data.dtype.byteorder == '>' or (data.dtype.byteorder == '=' and
                                           sys.byteorder == 'big'):
            data = data.byteswap()
        _array_tofile(fid, data)

        # Determine file size and place it in correct
        # position at start of the file or the data chunk.
        size = fid.tell()
        if not is_rf64:
            fid.seek(4)
            fid.write(struct.pack('<I', size-8))
        else:
            fid.seek(20)
            fid.write(struct.pack('<Q', size-8))

    finally:
        if not hasattr(filename, 'write'):
            fid.close()
        else:
            fid.seek(0)


def write(path, data, kind="OTHER", dohex=False):
    assertType1(data)
    kind = kind.upper()
    try:
        os.remove(path)
    except os.error:
        pass
    err = 1
    try:
        if kind == "LWFN":
            writeLWFN(path, data)
        elif kind == "PFB":
            writePFB(path, data)
        else:
            writeOther(path, data, dohex)
        err = 0
    finally:
        if err and not DEBUG:
            try:
                os.remove(path)
            except os.error:
                pass

