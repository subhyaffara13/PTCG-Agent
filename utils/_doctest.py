
def _doctest(*paths, **kwargs):
    """
    Internal function that actually runs the doctests.

    All keyword arguments from ``doctest()`` are passed to this function
    except for ``subprocess``.

    Returns 0 if tests passed and 1 if they failed.  See the docstrings of
    ``doctest()`` and ``test()`` for more information.
    """
    from sympy.printing.pretty.pretty import pprint_use_unicode
    from sympy.printing.pretty import stringpict

    normal = kwargs.get("normal", False)
    verbose = kwargs.get("verbose", False)
    colors = kwargs.get("colors", True)
    force_colors = kwargs.get("force_colors", False)
    blacklist = kwargs.get("blacklist", [])
    split  = kwargs.get('split', None)

    blacklist.extend(_get_doctest_blacklist())

    # Use a non-windowed backend, so that the tests work on CI
    if import_module('matplotlib') is not None:
        import matplotlib
        matplotlib.use('Agg')

    # Disable warnings for external modules
    import sympy.external
    sympy.external.importtools.WARN_OLD_VERSION = False
    sympy.external.importtools.WARN_NOT_INSTALLED = False

    # Disable showing up of plots
    from sympy.plotting.plot import unset_show
    unset_show()

    r = PyTestReporter(verbose, split=split, colors=colors,\
                       force_colors=force_colors)
    t = SymPyDocTests(r, normal)

    test_files = t.get_test_files('sympy')
    test_files.extend(t.get_test_files('examples', init_only=False))

    not_blacklisted = [f for f in test_files
                       if not any(b in f for b in blacklist)]
    if len(paths) == 0:
        matched = not_blacklisted
    else:
        # take only what was requested...but not blacklisted items
        # and allow for partial match anywhere or fnmatch of name
        paths = convert_to_native_paths(paths)
        matched = []
        for f in not_blacklisted:
            basename = os.path.basename(f)
            for p in paths:
                if p in f or fnmatch(basename, p):
                    matched.append(f)
                    break

    matched.sort()

    if split:
        matched = split_list(matched, split)

    t._testfiles.extend(matched)

    # run the tests and record the result for this *py portion of the tests
    if t._testfiles:
        failed = not t.test()
    else:
        failed = False

    # N.B.
    # --------------------------------------------------------------------
    # Here we test *.rst and *.md files at or below doc/src. Code from these
    # must be self supporting in terms of imports since there is no importing
    # of necessary modules by doctest.testfile. If you try to pass *.py files
    # through this they might fail because they will lack the needed imports
    # and smarter parsing that can be done with source code.
    #
    test_files_rst = t.get_test_files('doc/src', '*.rst', init_only=False)
    test_files_md = t.get_test_files('doc/src', '*.md', init_only=False)
    test_files = test_files_rst + test_files_md
    test_files.sort()

    not_blacklisted = [f for f in test_files
                       if not any(b in f for b in blacklist)]

    if len(paths) == 0:
        matched = not_blacklisted
    else:
        # Take only what was requested as long as it's not on the blacklist.
        # Paths were already made native in *py tests so don't repeat here.
        # There's no chance of having a *py file slip through since we
        # only have *rst files in test_files.
        matched = []
        for f in not_blacklisted:
            basename = os.path.basename(f)
            for p in paths:
                if p in f or fnmatch(basename, p):
                    matched.append(f)
                    break

    if split:
        matched = split_list(matched, split)

    first_report = True
    for rst_file in matched:
        if not os.path.isfile(rst_file):
            continue
        old_displayhook = sys.displayhook
        try:
            use_unicode_prev, wrap_line_prev = setup_pprint()
            out = sympytestfile(
                rst_file, module_relative=False, encoding='utf-8',
                optionflags=pdoctest.ELLIPSIS | pdoctest.NORMALIZE_WHITESPACE |
                pdoctest.IGNORE_EXCEPTION_DETAIL)
        finally:
            # make sure we return to the original displayhook in case some
            # doctest has changed that
            sys.displayhook = old_displayhook
            # The NO_GLOBAL flag overrides the no_global flag to init_printing
            # if True
            import sympy.interactive.printing as interactive_printing
            interactive_printing.NO_GLOBAL = False
            pprint_use_unicode(use_unicode_prev)
            stringpict._GLOBAL_WRAP_LINE = wrap_line_prev

        rstfailed, tested = out
        if tested:
            failed = rstfailed or failed
            if first_report:
                first_report = False
                msg = 'rst/md doctests start'
                if not t._testfiles:
                    r.start(msg=msg)
                else:
                    r.write_center(msg)
                    print()
            # use as the id, everything past the first 'sympy'
            file_id = rst_file[rst_file.find('sympy') + len('sympy') + 1:]
            print(file_id, end=" ")
                # get at least the name out so it is know who is being tested
            wid = r.terminal_width - len(file_id) - 1  # update width
            test_file = '[%s]' % (tested)
            report = '[%s]' % (rstfailed or 'OK')
            print(''.join(
                [test_file, ' '*(wid - len(test_file) - len(report)), report])
            )

    # the doctests for *py will have printed this message already if there was
    # a failure, so now only print it if there was intervening reporting by
    # testing the *rst as evidenced by first_report no longer being True.
    if not first_report and failed:
        print()
        print("DO *NOT* COMMIT!")

    return int(failed)

