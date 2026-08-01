
def theq(a, b):
    """ Test two Aesara objects for equality.

    Also accepts numeric types and lists/tuples of supported types.

    Note - debugprint() has a bug where it will accept numeric types but does
    not respect the "file" argument and in this case and instead prints the number
    to stdout and returns an empty string. This can lead to tests passing where
    they should fail because any two numbers will always compare as equal. To
    prevent this we treat numbers as a separate case.
    """
    numeric_types = (int, float, np.number)
    a_is_num = isinstance(a, numeric_types)
    b_is_num = isinstance(b, numeric_types)

    # Compare numeric types using regular equality
    if a_is_num or b_is_num:
        if not (a_is_num and b_is_num):
            return False

        return a == b

    # Compare sequences element-wise
    a_is_seq = isinstance(a, (tuple, list))
    b_is_seq = isinstance(b, (tuple, list))

    if a_is_seq or b_is_seq:
        if not (a_is_seq and b_is_seq) or type(a) != type(b):
            return False

        return list(map(theq, a)) == list(map(theq, b))

    # Otherwise, assume debugprint() can handle it
    astr = aesara.printing.debugprint(a, file='str')
    bstr = aesara.printing.debugprint(b, file='str')

    # Check for bug mentioned above
    for argname, argval, argstr in [('a', a, astr), ('b', b, bstr)]:
        if argstr == '':
            raise TypeError(
                'aesara.printing.debugprint(%s) returned empty string '
                '(%s is instance of %r)'
                % (argname, argname, type(argval))
            )

    return astr == bstr


def theq(a, b):
    """ Test two Theano objects for equality.

    Also accepts numeric types and lists/tuples of supported types.

    Note - debugprint() has a bug where it will accept numeric types but does
    not respect the "file" argument and in this case and instead prints the number
    to stdout and returns an empty string. This can lead to tests passing where
    they should fail because any two numbers will always compare as equal. To
    prevent this we treat numbers as a separate case.
    """
    numeric_types = (int, float, np.number)
    a_is_num = isinstance(a, numeric_types)
    b_is_num = isinstance(b, numeric_types)

    # Compare numeric types using regular equality
    if a_is_num or b_is_num:
        if not (a_is_num and b_is_num):
            return False

        return a == b

    # Compare sequences element-wise
    a_is_seq = isinstance(a, (tuple, list))
    b_is_seq = isinstance(b, (tuple, list))

    if a_is_seq or b_is_seq:
        if not (a_is_seq and b_is_seq) or type(a) != type(b):
            return False

        return list(map(theq, a)) == list(map(theq, b))

    # Otherwise, assume debugprint() can handle it
    astr = theano.printing.debugprint(a, file='str')
    bstr = theano.printing.debugprint(b, file='str')

    # Check for bug mentioned above
    for argname, argval, argstr in [('a', a, astr), ('b', b, bstr)]:
        if argstr == '':
            raise TypeError(
                'theano.printing.debugprint(%s) returned empty string '
                '(%s is instance of %r)'
                % (argname, argname, type(argval))
            )

    return astr == bstr

