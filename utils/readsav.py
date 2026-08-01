
def readsav(file_name, idict=None, python_dict=False,
            uncompressed_file_name=None, verbose=False):
    """
    Read an IDL .sav file.

    Parameters
    ----------
    file_name : str
        Name of the IDL save file.
    idict : dict, optional
        Dictionary in which to insert .sav file variables.
    python_dict : bool, optional
        By default, the object return is not a Python dictionary, but a
        case-insensitive dictionary with item, attribute, and call access
        to variables. To get a standard Python dictionary, set this option
        to True.
    uncompressed_file_name : str, optional
        This option only has an effect for .sav files written with the
        /compress option. If a file name is specified, compressed .sav
        files are uncompressed to this file. Otherwise, readsav will use
        the `tempfile` module to determine a temporary filename
        automatically, and will remove the temporary file upon successfully
        reading it in.
    verbose : bool, optional
        Whether to print out information about the save file, including
        the records read, and available variables.

    Returns
    -------
    idl_dict : AttrDict or dict
        If `python_dict` is set to False (default), this function returns a
        case-insensitive dictionary with item, attribute, and call access
        to variables. If `python_dict` is set to True, this function
        returns a Python dictionary with all variable names in lowercase.
        If `idict` was specified, then variables are written to the
        dictionary specified, and the updated dictionary is returned.

    Examples
    --------
    >>> from os.path import dirname, join as pjoin
    >>> import scipy.io as sio
    >>> from scipy.io import readsav

    Get the filename for an example .sav file from the tests/data directory.

    >>> data_dir = pjoin(dirname(sio.__file__), 'tests', 'data')
    >>> sav_fname = pjoin(data_dir, 'array_float32_1d.sav')

    Load the .sav file contents.

    >>> sav_data = readsav(sav_fname)

    Get keys of the .sav file contents.

    >>> print(sav_data.keys())
    dict_keys(['array1d'])

    Access a content with a key.

    >>> print(sav_data['array1d'])
    [0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.
     0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.
     0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.
     0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.
     0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0. 0.
     0. 0. 0.]

    """

    # Initialize record and variable holders
    records = []
    if python_dict or idict:
        variables = {}
    else:
        variables = AttrDict()

    # Open the IDL file
    f = open(file_name, 'rb')

    # Read the signature, which should be 'SR'
    signature = _read_bytes(f, 2)
    if signature != b'SR':
        raise Exception(f"Invalid SIGNATURE: {signature}")

    # Next, the record format, which is '\x00\x04' for normal .sav
    # files, and '\x00\x06' for compressed .sav files.
    recfmt = _read_bytes(f, 2)

    if recfmt == b'\x00\x04':
        pass

    elif recfmt == b'\x00\x06':

        if verbose:
            print("IDL Save file is compressed")

        if uncompressed_file_name:
            fout = open(uncompressed_file_name, 'w+b')
        else:
            fout = tempfile.NamedTemporaryFile(suffix='.sav')

        if verbose:
            print(f" -> expanding to {fout.name}")

        # Write header
        fout.write(b'SR\x00\x04')

        # Cycle through records
        while True:

            # Read record type
            rectype = _read_long(f)
            fout.write(struct.pack('>l', int(rectype)))

            # Read position of next record and return as int
            nextrec = _read_uint32(f)
            nextrec += _read_uint32(f).astype(np.int64) * 2**32

            # Read the unknown 4 bytes
            unknown = f.read(4)

            # Check if the end of the file has been reached
            if RECTYPE_DICT[rectype] == 'END_MARKER':
                modval = np.int64(2**32)
                fout.write(struct.pack('>I', int(nextrec) % modval))
                fout.write(
                    struct.pack('>I', int((nextrec - (nextrec % modval)) / modval))
                )
                fout.write(unknown)
                break

            # Find current position
            pos = f.tell()

            # Decompress record
            rec_string = zlib.decompress(f.read(nextrec-pos))

            # Find new position of next record
            nextrec = fout.tell() + len(rec_string) + 12

            # Write out record
            fout.write(struct.pack('>I', int(nextrec % 2**32)))
            fout.write(struct.pack('>I', int((nextrec - (nextrec % 2**32)) / 2**32)))
            fout.write(unknown)
            fout.write(rec_string)

        # Close the original compressed file
        f.close()

        # Set f to be the decompressed file, and skip the first four bytes
        f = fout
        f.seek(4)

    else:
        raise Exception(f"Invalid RECFMT: {recfmt}")

    # Loop through records, and add them to the list
    while True:
        r = _read_record(f)
        records.append(r)
        if 'end' in r:
            if r['end']:
                break

    # Close the file
    f.close()

    # Find heap data variables
    heap = {}
    for r in records:
        if r['rectype'] == "HEAP_DATA":
            heap[r['heap_index']] = r['data']

    # Find all variables
    for r in records:
        if r['rectype'] == "VARIABLE":
            replace, new = _replace_heap(r['data'], heap)
            if replace:
                r['data'] = new
            variables[r['varname'].lower()] = r['data']

    if verbose:

        # Print out timestamp info about the file
        for record in records:
            if record['rectype'] == "TIMESTAMP":
                print("-"*50)
                print(f"Date: {record['date']}")
                print(f"User: {record['user']}")
                print(f"Host: {record['host']}")
                break

        # Print out version info about the file
        for record in records:
            if record['rectype'] == "VERSION":
                print("-"*50)
                print(f"Format: {record['format']}")
                print(f"Architecture: {record['arch']}")
                print(f"Operating System: {record['os']}")
                print(f"IDL Version: {record['release']}")
                break

        # Print out identification info about the file
        for record in records:
            if record['rectype'] == "IDENTIFICATION":
                print("-"*50)
                print(f"Author: {record['author']}")
                print(f"Title: {record['title']}")
                print(f"ID Code: {record['idcode']}")
                break

        # Print out descriptions saved with the file
        for record in records:
            if record['rectype'] == "DESCRIPTION":
                print("-"*50)
                print(f"Description: {record['description']}")
                break

        print("-"*50)
        print(f"Successfully read {len(records)} records of which:")

        # Create convenience list of record types
        rectypes = [r['rectype'] for r in records]

        for rt in set(rectypes):
            if rt != 'END_MARKER':
                print(f" - {rectypes.count(rt)} are of type {rt}")
        print("-"*50)

        if 'VARIABLE' in rectypes:
            print("Available variables:")
            for var in variables:
                print(f" - {var} [{type(variables[var])}]")
            print("-"*50)

    if idict:
        for var in variables:
            idict[var] = variables[var]
        return idict
    else:
        return variables

