
def _loadarff(ofile):
    # Parse the header file
    try:
        rel, attr = read_header(ofile)
    except ValueError as e:
        msg = "Error while parsing header, error was: " + str(e)
        raise ParseArffError(msg) from e

    # Check whether we have a string attribute (not supported yet)
    hasstr = False
    for a in attr:
        if isinstance(a, StringAttribute):
            hasstr = True

    meta = MetaData(rel, attr)

    # XXX The following code is not great
    # Build the type descriptor descr and the list of converters to convert
    # each attribute to the suitable type (which should match the one in
    # descr).

    # This can be used once we want to support integer as integer values and
    # not as numeric anymore (using masked arrays ?).

    if hasstr:
        # How to support string efficiently ? Ideally, we should know the max
        # size of the string before allocating the numpy array.
        raise NotImplementedError("String attributes not supported yet, sorry")

    ni = len(attr)

    def generator(row_iter, delim=','):
        # TODO: this is where we are spending time (~80%). I think things
        # could be made more efficiently:
        #   - We could for example "compile" the function, because some values
        #   do not change here.
        #   - The function to convert a line to dtyped values could also be
        #   generated on the fly from a string and be executed instead of
        #   looping.
        #   - The regex are overkill: for comments, checking that a line starts
        #   by % should be enough and faster, and for empty lines, same thing
        #   --> this does not seem to change anything.

        # 'compiling' the range since it does not change
        # Note, I have already tried zipping the converters and
        # row elements and got slightly worse performance.
        elems = list(range(ni))

        dialect = None
        for raw in row_iter:
            # We do not abstract skipping comments and empty lines for
            # performance reasons.
            if r_comment.match(raw) or r_empty.match(raw):
                continue

            row, dialect = split_data_line(raw, dialect)

            yield tuple([attr[i].parse_data(row[i]) for i in elems])

    a = list(generator(ofile))
    # No error should happen here: it is a bug otherwise
    data = np.array(a, [(a.name, a.dtype) for a in attr])
    return data, meta

