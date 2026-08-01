
def autowrap(expr, language=None, backend='f2py', tempdir=None, args=None,
             flags=None, verbose=False, helpers=None, code_gen=None, **kwargs):
    """Generates Python callable binaries based on the math expression.

    Parameters
    ==========

    expr
        The SymPy expression that should be wrapped as a binary routine.
    language : string, optional
        If supplied, (options: 'C' or 'F95'), specifies the language of the
        generated code. If ``None`` [default], the language is inferred based
        upon the specified backend.
    backend : string, optional
        Backend used to wrap the generated code. Either 'f2py' [default],
        or 'cython'.
    tempdir : string, optional
        Path to directory for temporary files. If this argument is supplied,
        the generated code and the wrapper input files are left intact in the
        specified path.
    args : iterable, optional
        An ordered iterable of symbols. Specifies the argument sequence for the
        function.
    flags : iterable, optional
        Additional option flags that will be passed to the backend.
    verbose : bool, optional
        If True, autowrap will not mute the command line backends. This can be
        helpful for debugging.
    helpers : 3-tuple or iterable of 3-tuples, optional
        Used to define auxiliary functions needed for the main expression.
        Each tuple should be of the form (name, expr, args) where:

        - name : str, the function name
        - expr : sympy expression, the function
        - args : iterable, the function arguments (can be any iterable of symbols)

    code_gen : CodeGen instance
        An instance of a CodeGen subclass. Overrides ``language``.
    include_dirs : [string]
        A list of directories to search for C/C++ header files (in Unix form
        for portability).
    library_dirs : [string]
        A list of directories to search for C/C++ libraries at link time.
    libraries : [string]
        A list of library names (not filenames or paths) to link against.
    extra_compile_args : [string]
        Any extra platform- and compiler-specific information to use when
        compiling the source files in 'sources'.  For platforms and compilers
        where "command line" makes sense, this is typically a list of
        command-line arguments, but for other platforms it could be anything.
    extra_link_args : [string]
        Any extra platform- and compiler-specific information to use when
        linking object files together to create the extension (or to create a
        new static Python interpreter).  Similar interpretation as for
        'extra_compile_args'.

    Examples
    ========

    Basic usage:

    >>> from sympy.abc import x, y, z
    >>> from sympy.utilities.autowrap import autowrap
    >>> expr = ((x - y + z)**(13)).expand()
    >>> binary_func = autowrap(expr)
    >>> binary_func(1, 4, 2)
    -1.0

    Using helper functions:

    >>> from sympy.abc import x, t
    >>> from sympy import Function
    >>> helper_func = Function('helper_func')  # Define symbolic function
    >>> expr = 3*x + helper_func(t)  # Main expression using helper function
    >>> # Define helper_func(x) = 4*x using f2py backend
    >>> binary_func = autowrap(expr, args=[x, t],
    ...                       helpers=('helper_func', 4*x, [x]))
    >>> binary_func(2, 5)  # 3*2 + helper_func(5) = 6 + 20
    26.0
    >>> # Same example using cython backend
    >>> binary_func = autowrap(expr, args=[x, t], backend='cython',
    ...                       helpers=[('helper_func', 4*x, [x])])
    >>> binary_func(2, 5)  # 3*2 + helper_func(5) = 6 + 20
    26.0

    Type handling example:

    >>> import numpy as np
    >>> expr = x + y
    >>> f_cython = autowrap(expr, backend='cython')
    >>> f_cython(1, 2)  # doctest: +ELLIPSIS
    Traceback (most recent call last):
      ...
    TypeError: Argument '_x' has incorrect type (expected numpy.ndarray, got int)
    >>> f_cython(np.array([1.0]), np.array([2.0]))
    array([ 3.])

    """
    if language:
        if not isinstance(language, type):
            _validate_backend_language(backend, language)
    else:
        language = _infer_language(backend)

    # two cases 1) helpers is an iterable of 3-tuples and 2) helpers is a
    # 3-tuple
    if iterable(helpers) and len(helpers) != 0 and iterable(helpers[0]):
        helpers = helpers if helpers else ()
    else:
        helpers = [helpers] if helpers else ()
    args = list(args) if iterable(args, exclude=set) else args

    if code_gen is None:
        code_gen = get_code_generator(language, "autowrap")

    CodeWrapperClass = {
        'F2PY': F2PyCodeWrapper,
        'CYTHON': CythonCodeWrapper,
        'DUMMY': DummyWrapper
    }[backend.upper()]
    code_wrapper = CodeWrapperClass(code_gen, tempdir, flags if flags else (),
                                    verbose, **kwargs)

    helps = []
    for name_h, expr_h, args_h in helpers:
        helps.append(code_gen.routine(name_h, expr_h, args_h))

    for name_h, expr_h, args_h in helpers:
        if expr.has(expr_h):
            name_h = binary_function(name_h, expr_h, backend='dummy')
            expr = expr.subs(expr_h, name_h(*args_h))
    try:
        routine = code_gen.routine('autofunc', expr, args)
    except CodeGenArgumentListError as e:
        # if all missing arguments are for pure output, we simply attach them
        # at the end and try again, because the wrappers will silently convert
        # them to return values anyway.
        new_args = []
        for missing in e.missing_args:
            if not isinstance(missing, OutputArgument):
                raise
            new_args.append(missing.name)
        routine = code_gen.routine('autofunc', expr, args + new_args)

    return code_wrapper.wrap_code(routine, helpers=helps)

