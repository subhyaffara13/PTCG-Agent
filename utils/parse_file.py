
def parse_file(
    filename, use_cpp=False, cpp_path="cpp", cpp_args="", parser=None, encoding=None
):
    """Parse a C file using pycparser.

    filename:
        Name of the file you want to parse.

    use_cpp:
        Set to True if you want to execute the C pre-processor
        on the file prior to parsing it.

    cpp_path:
        If use_cpp is True, this is the path to 'cpp' on your
        system. If no path is provided, it attempts to just
        execute 'cpp', so it must be in your PATH.

    cpp_args:
        If use_cpp is True, set this to the command line arguments strings
        to cpp. Be careful with quotes - it's best to pass a raw string
        (r'') here. For example:
        r'-I../utils/fake_libc_include'
        If several arguments are required, pass a list of strings.

    encoding:
        Encoding to use for the file to parse

    parser:
        Optional parser object to be used instead of the default CParser

    When successful, an AST is returned. ParseError can be
    thrown if the file doesn't parse successfully.

    Errors from cpp will be printed out.
    """
    if use_cpp:
        text = preprocess_file(filename, cpp_path, cpp_args)
    else:
        with io.open(filename, encoding=encoding) as f:
            text = f.read()

    if parser is None:
        parser = CParser()
    return parser.parse(text, filename)

