
def run_compile():
    """
    Do it all in one call!
    """
    import tempfile

    # Collect dependency flags, preprocess sys.argv
    argy = preparse_sysargv()
    modulename = argy["modulename"]
    if modulename is None:
        modulename = 'untitled'
    dependencies = argy["dependencies"]
    backend_key = argy["backend"]
    build_backend = f2py_build_generator(backend_key)

    i = sys.argv.index('-c')
    del sys.argv[i]

    remove_build_dir = 0
    try:
        i = sys.argv.index('--build-dir')
    except ValueError:
        i = None
    if i is not None:
        build_dir = sys.argv[i + 1]
        del sys.argv[i + 1]
        del sys.argv[i]
    else:
        remove_build_dir = 1
        build_dir = tempfile.mkdtemp()

    _reg1 = re.compile(r'--link-')
    sysinfo_flags = [_m for _m in sys.argv[1:] if _reg1.match(_m)]
    sys.argv = [_m for _m in sys.argv if _m not in sysinfo_flags]
    if sysinfo_flags:
        sysinfo_flags = [f[7:] for f in sysinfo_flags]

    _reg2 = re.compile(
        r'--((no-|)(wrap-functions|lower|freethreading-compatible|latex-doc)|debug-capi|quiet|skip-empty-wrappers)|-include')
    f2py_flags = [_m for _m in sys.argv[1:] if _reg2.match(_m)]
    sys.argv = [_m for _m in sys.argv if _m not in f2py_flags]
    f2py_flags2 = []
    fl = 0
    for a in sys.argv[1:]:
        if a in ['only:', 'skip:']:
            fl = 1
        elif a == ':':
            fl = 0
        if fl or a == ':':
            f2py_flags2.append(a)
    if f2py_flags2 and f2py_flags2[-1] != ':':
        f2py_flags2.append(':')
    f2py_flags.extend(f2py_flags2)
    sys.argv = [_m for _m in sys.argv if _m not in f2py_flags2]
    _reg3 = re.compile(
        r'--((f(90)?compiler(-exec|)|compiler)=|help-compiler)')
    flib_flags = [_m for _m in sys.argv[1:] if _reg3.match(_m)]
    sys.argv = [_m for _m in sys.argv if _m not in flib_flags]
    # TODO: Once distutils is dropped completely, i.e. min_ver >= 3.12, unify into --fflags
    reg_f77_f90_flags = re.compile(r'--f(77|90)flags=')
    reg_distutils_flags = re.compile(r'--((f(77|90)exec|opt|arch)=|(debug|noopt|noarch|help-fcompiler))')
    fc_flags = [_m for _m in sys.argv[1:] if reg_f77_f90_flags.match(_m)]
    distutils_flags = [_m for _m in sys.argv[1:] if reg_distutils_flags.match(_m)]
    sys.argv = [_m for _m in sys.argv if _m not in (fc_flags + distutils_flags)]

    del_list = []
    for s in flib_flags:
        v = '--fcompiler='
        if s[:len(v)] == v:
            outmess(
                "--fcompiler cannot be used with meson,"
                "set compiler with the FC environment variable\n"
                )
    for s in del_list:
        i = flib_flags.index(s)
        del flib_flags[i]
    assert len(flib_flags) <= 2, repr(flib_flags)

    _reg5 = re.compile(r'--(verbose)')
    setup_flags = [_m for _m in sys.argv[1:] if _reg5.match(_m)]
    sys.argv = [_m for _m in sys.argv if _m not in setup_flags]

    if '--quiet' in f2py_flags:
        setup_flags.append('--quiet')

    # Ugly filter to remove everything but sources
    sources = sys.argv[1:]
    f2cmapopt = '--f2cmap'
    if f2cmapopt in sys.argv:
        i = sys.argv.index(f2cmapopt)
        f2py_flags.extend(sys.argv[i:i + 2])
        del sys.argv[i + 1], sys.argv[i]
        sources = sys.argv[1:]

    pyf_files, _sources = filter_files("", "[.]pyf([.]src|)", sources)
    sources = pyf_files + _sources
    modulename = validate_modulename(pyf_files, modulename)
    extra_objects, sources = filter_files('', '[.](o|a|so|dylib)', sources)
    library_dirs, sources = filter_files('-L', '', sources, remove_prefix=1)
    libraries, sources = filter_files('-l', '', sources, remove_prefix=1)
    undef_macros, sources = filter_files('-U', '', sources, remove_prefix=1)
    define_macros, sources = filter_files('-D', '', sources, remove_prefix=1)
    for i in range(len(define_macros)):
        name_value = define_macros[i].split('=', 1)
        if len(name_value) == 1:
            name_value.append(None)
        if len(name_value) == 2:
            define_macros[i] = tuple(name_value)
        else:
            print('Invalid use of -D:', name_value)

    # Construct wrappers / signatures / things
    if backend_key == 'meson':
        if not pyf_files:
            outmess('Using meson backend\nWill pass --lower to f2py\nSee https://numpy.org/doc/stable/f2py/buildtools/meson.html\n')
            f2py_flags.append('--lower')
            run_main(f" {' '.join(f2py_flags)} -m {modulename} {' '.join(sources)}".split())
        else:
            run_main(f" {' '.join(f2py_flags)} {' '.join(pyf_files)}".split())

    # Order matters here, includes are needed for run_main above
    include_dirs, _, sources = get_newer_options(sources)
    # Now use the builder
    builder = build_backend(
        modulename,
        sources,
        extra_objects,
        build_dir,
        include_dirs,
        library_dirs,
        libraries,
        define_macros,
        undef_macros,
        f2py_flags,
        sysinfo_flags,
        fc_flags,
        flib_flags,
        setup_flags,
        remove_build_dir,
        {"dependencies": dependencies},
    )

    builder.compile()

