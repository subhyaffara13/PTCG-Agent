
def autoparse(
        func=None, *,
        description=None,
        epilog=None,
        add_nos=False,
        parser=None):
    '''
    This decorator converts a function that takes normal arguments into a
    function which takes a single optional argument, argv, parses it using an
    argparse.ArgumentParser, and calls the underlying function with the parsed
    arguments. If it is not given, sys.argv[1:] is used. This is so that the
    function can be used as a setuptools entry point, as well as a normal main
    function. sys.argv[1:] is not evaluated until the function is called, to
    allow injecting different arguments for testing.

    It uses the argument signature of the function to create an
    ArgumentParser. Parameters without defaults become positional parameters,
    while parameters *with* defaults become --options. Use annotations to set
    the type of the parameter.

    The `desctiption` and `epilog` parameters corrospond to the same respective
    argparse parameters. If no description is given, it defaults to the
    decorated functions's docstring, if present.

    If add_nos is True, every boolean option (that is, every parameter with a
    default of True/False or a type of bool) will have a --no- version created
    as well, which inverts the option. For instance, the --verbose option will
    have a --no-verbose counterpart. These are not mutually exclusive-
    whichever one appears last in the argument list will have precedence.

    If a parser is given, it is used instead of one generated from the function
    signature. In this case, no parser is created; instead, the given parser is
    used to parse the argv argument. The parser's results' argument names must
    match up with the parameter names of the decorated function.

    The decorated function is attached to the result as the `func` attribute,
    and the parser is attached as the `parser` attribute.
    '''

    # If @autoparse(...) is used instead of @autoparse
    if func is None:
        return lambda f: autoparse(
            f, description=description,
            epilog=epilog,
            add_nos=add_nos,
            parser=parser)

    func_sig = signature(func)

    docstr_description, docstr_epilog = parse_docstring(getdoc(func))

    if parser is None:
        parser = make_parser(
            func_sig,
            description or docstr_description,
            epilog or docstr_epilog,
            add_nos)

    @wraps(func)
    def autoparse_wrapper(argv=None):
        if argv is None:
            argv = sys.argv[1:]

        # Get empty argument binding, to fill with parsed arguments. This
        # object does all the heavy lifting of turning named arguments into
        # into correctly bound *args and **kwargs.
        parsed_args = func_sig.bind_partial()
        parsed_args.arguments.update(vars(parser.parse_args(argv)))

        return func(*parsed_args.args, **parsed_args.kwargs)

    # TODO: attach an updated __signature__ to autoparse_wrapper, just in case.

    # Attach the wrapped function and parser, and return the wrapper.
    autoparse_wrapper.func = func
    autoparse_wrapper.parser = parser
    return autoparse_wrapper

