
def test(*paths, subprocess=True, rerun=0, **kwargs):
    """
    Run tests in the specified test_*.py files.

    Tests in a particular test_*.py file are run if any of the given strings
    in ``paths`` matches a part of the test file's path. If ``paths=[]``,
    tests in all test_*.py files are run.

    Notes:

    - If sort=False, tests are run in random order (not default).
    - Paths can be entered in native system format or in unix,
      forward-slash format.
    - Files that are on the blacklist can be tested by providing
      their path; they are only excluded if no paths are given.

    **Explanation of test results**

    ======  ===============================================================
    Output  Meaning
    ======  ===============================================================
    .       passed
    F       failed
    X       XPassed (expected to fail but passed)
    f       XFAILed (expected to fail and indeed failed)
    s       skipped
    w       slow
    T       timeout (e.g., when ``--timeout`` is used)
    K       KeyboardInterrupt (when running the slow tests with ``--slow``,
            you can interrupt one of them without killing the test runner)
    ======  ===============================================================


    Colors have no additional meaning and are used just to facilitate
    interpreting the output.

    Examples
    ========

    >>> import sympy

    Run all tests:

    >>> sympy.test()    # doctest: +SKIP

    Run one file:

    >>> sympy.test("sympy/core/tests/test_basic.py")    # doctest: +SKIP
    >>> sympy.test("_basic")    # doctest: +SKIP

    Run all tests in sympy/functions/ and some particular file:

    >>> sympy.test("sympy/core/tests/test_basic.py",
    ...        "sympy/functions")    # doctest: +SKIP

    Run all tests in sympy/core and sympy/utilities:

    >>> sympy.test("/core", "/util")    # doctest: +SKIP

    Run specific test from a file:

    >>> sympy.test("sympy/core/tests/test_basic.py",
    ...        kw="test_equality")    # doctest: +SKIP

    Run specific test from any file:

    >>> sympy.test(kw="subs")    # doctest: +SKIP

    Run the tests with verbose mode on:

    >>> sympy.test(verbose=True)    # doctest: +SKIP

    Do not sort the test output:

    >>> sympy.test(sort=False)    # doctest: +SKIP

    Turn on post-mortem pdb:

    >>> sympy.test(pdb=True)    # doctest: +SKIP

    Turn off colors:

    >>> sympy.test(colors=False)    # doctest: +SKIP

    Force colors, even when the output is not to a terminal (this is useful,
    e.g., if you are piping to ``less -r`` and you still want colors)

    >>> sympy.test(force_colors=False)    # doctest: +SKIP

    The traceback verboseness can be set to "short" or "no" (default is
    "short")

    >>> sympy.test(tb='no')    # doctest: +SKIP

    The ``split`` option can be passed to split the test run into parts. The
    split currently only splits the test files, though this may change in the
    future. ``split`` should be a string of the form 'a/b', which will run
    part ``a`` of ``b``. For instance, to run the first half of the test suite:

    >>> sympy.test(split='1/2')  # doctest: +SKIP

    The ``time_balance`` option can be passed in conjunction with ``split``.
    If ``time_balance=True`` (the default for ``sympy.test``), SymPy will attempt
    to split the tests such that each split takes equal time.  This heuristic
    for balancing is based on pre-recorded test data.

    >>> sympy.test(split='1/2', time_balance=True)  # doctest: +SKIP

    You can disable running the tests in a separate subprocess using
    ``subprocess=False``.  This is done to support seeding hash randomization,
    which is enabled by default in the Python versions where it is supported.
    If subprocess=False, hash randomization is enabled/disabled according to
    whether it has been enabled or not in the calling Python process.
    However, even if it is enabled, the seed cannot be printed unless it is
    called from a new Python process.

    Hash randomization was added in the minor Python versions 2.6.8, 2.7.3,
    3.1.5, and 3.2.3, and is enabled by default in all Python versions after
    and including 3.3.0.

    If hash randomization is not supported ``subprocess=False`` is used
    automatically.

    >>> sympy.test(subprocess=False)     # doctest: +SKIP

    To set the hash randomization seed, set the environment variable
    ``PYTHONHASHSEED`` before running the tests.  This can be done from within
    Python using

    >>> import os
    >>> os.environ['PYTHONHASHSEED'] = '42' # doctest: +SKIP

    Or from the command line using

    $ PYTHONHASHSEED=42 ./bin/test

    If the seed is not set, a random seed will be chosen.

    Note that to reproduce the same hash values, you must use both the same seed
    as well as the same architecture (32-bit vs. 64-bit).

    """
    # count up from 0, do not print 0
    print_counter = lambda i : (print("rerun %d" % (rerun-i))
                                if rerun-i else None)

    if subprocess:
        # loop backwards so last i is 0
        for i in range(rerun, -1, -1):
            print_counter(i)
            ret = run_in_subprocess_with_hash_randomization("_test",
                        function_args=paths, function_kwargs=kwargs)
            if ret is False:
                break
            val = not bool(ret)
            # exit on the first failure or if done
            if not val or i == 0:
                return val

    # rerun even if hash randomization is not supported
    for i in range(rerun, -1, -1):
        print_counter(i)
        val = not bool(_test(*paths, **kwargs))
        if not val or i == 0:
            return val


def test(*paths, subprocess=True, rerun=0, **kwargs):
    """Interface to run tests via pytest compatible with SymPy's test runner.

    Explanation
    ===========

    Note that a `pytest.ExitCode`, which is an `enum`, is returned. This is
    different to the legacy SymPy test runner which would return a `bool`. If
    all tests successfully pass the `pytest.ExitCode.OK` with value `0` is
    returned, whereas the legacy SymPy test runner would return `True`. In any
    other scenario, a non-zero `enum` value is returned, whereas the legacy
    SymPy test runner would return `False`. Users need to, therefore, be careful
    if treating the pytest exit codes as booleans because
    `bool(pytest.ExitCode.OK)` evaluates to `False`, the opposite of legacy
    behaviour.

    Examples
    ========

    >>> import sympy  # doctest: +SKIP

    Run one file:

    >>> sympy.test('sympy/core/tests/test_basic.py')  # doctest: +SKIP
    >>> sympy.test('_basic')  # doctest: +SKIP

    Run all tests in sympy/functions/ and some particular file:

    >>> sympy.test("sympy/core/tests/test_basic.py",
    ...            "sympy/functions")  # doctest: +SKIP

    Run all tests in sympy/core and sympy/utilities:

    >>> sympy.test("/core", "/util")  # doctest: +SKIP

    Run specific test from a file:

    >>> sympy.test("sympy/core/tests/test_basic.py",
    ...            kw="test_equality")  # doctest: +SKIP

    Run specific test from any file:

    >>> sympy.test(kw="subs")  # doctest: +SKIP

    Run the tests using the legacy SymPy runner:

    >>> sympy.test(use_sympy_runner=True)  # doctest: +SKIP

    Note that this option is slated for deprecation in the near future and is
    only currently provided to ensure users have an alternative option while the
    pytest-based runner receives real-world testing.

    Parameters
    ==========
    paths : first n positional arguments of strings
        Paths, both partial and absolute, describing which subset(s) of the test
        suite are to be run.
    subprocess : bool, default is True
        Legacy option, is currently ignored.
    rerun : int, default is 0
        Legacy option, is ignored.
    use_sympy_runner : bool or None, default is None
        Temporary option to invoke the legacy SymPy test runner instead of
        `pytest.main`. Will be removed in the near future.
    verbose : bool, default is False
        Sets the verbosity of the pytest output. Using `True` will add the
        `--verbose` option to the pytest call.
    tb : str, 'auto', 'long', 'short', 'line', 'native', or 'no'
        Sets the traceback print mode of pytest using the `--tb` option.
    kw : str
        Only run tests which match the given substring expression. An expression
        is a Python evaluatable expression where all names are substring-matched
        against test names and their parent classes. Example: -k 'test_method or
        test_other' matches all test functions and classes whose name contains
        'test_method' or 'test_other', while -k 'not test_method' matches those
        that don't contain 'test_method' in their names. -k 'not test_method and
        not test_other' will eliminate the matches. Additionally keywords are
        matched to classes and functions containing extra names in their
        'extra_keyword_matches' set, as well as functions which have names
        assigned directly to them. The matching is case-insensitive.
    pdb : bool, default is False
        Start the interactive Python debugger on errors or `KeyboardInterrupt`.
    colors : bool, default is True
        Color terminal output.
    force_colors : bool, default is False
        Legacy option, is ignored.
    sort : bool, default is True
        Run the tests in sorted order. pytest uses a sorted test order by
        default. Requires pytest-randomly.
    seed : int
        Seed to use for random number generation. Requires pytest-randomly.
    timeout : int, default is 0
        Timeout in seconds before dumping the stacks. 0 means no timeout.
        Requires pytest-timeout.
    fail_on_timeout : bool, default is False
        Legacy option, is currently ignored.
    slow : bool, default is False
        Run the subset of tests marked as `slow`.
    enhance_asserts : bool, default is False
        Legacy option, is currently ignored.
    split : string in form `<SPLIT>/<GROUPS>` or None, default is None
        Used to split the tests up. As an example, if `split='2/3' is used then
        only the middle third of tests are run. Requires pytest-split.
    time_balance : bool, default is True
        Legacy option, is currently ignored.
    blacklist : iterable of test paths as strings, default is BLACKLIST_DEFAULT
        Blacklisted test paths are ignored using the `--ignore` option. Paths
        may be partial or absolute. If partial then they are matched against
        all paths in the pytest tests path.
    parallel : bool, default is False
        Parallelize the test running using pytest-xdist. If `True` then pytest
        will automatically detect the number of CPU cores available and use them
        all. Requires pytest-xdist.
    store_durations : bool, False
        Store test durations into the file `.test_durations`. The is used by
        `pytest-split` to help determine more even splits when more than one
        test group is being used. Requires pytest-split.

    """
    # NOTE: to be removed alongside SymPy test runner
    if kwargs.get('use_sympy_runner', False):
        kwargs.pop('parallel', False)
        kwargs.pop('store_durations', False)
        kwargs.pop('use_sympy_runner', True)
        if kwargs.get('slow') is None:
            kwargs['slow'] = False
        return test_sympy(*paths, subprocess=True, rerun=0, **kwargs)

    pytest_plugin_manager = PytestPluginManager()
    if not pytest_plugin_manager.has_pytest:
        pytest.main()

    args = []

    if kwargs.get('verbose', False):
        args.append('--verbose')

    if tb := kwargs.get('tb'):
        args.extend(['--tb', tb])

    if kwargs.get('pdb'):
        args.append('--pdb')

    if not kwargs.get('colors', True):
        args.extend(['--color', 'no'])

    if seed := kwargs.get('seed'):
        if not pytest_plugin_manager.has_randomly:
            msg = '`pytest-randomly` plugin required to control random seed.'
            raise ModuleNotFoundError(msg)
        args.extend(['--randomly-seed', str(seed)])

    if kwargs.get('sort', True) and pytest_plugin_manager.has_randomly:
        args.append('--randomly-dont-reorganize')
    elif not kwargs.get('sort', True) and not pytest_plugin_manager.has_randomly:
        msg = '`pytest-randomly` plugin required to randomize test order.'
        raise ModuleNotFoundError(msg)

    if timeout := kwargs.get('timeout', None):
        if not pytest_plugin_manager.has_timeout:
            msg = '`pytest-timeout` plugin required to apply timeout to tests.'
            raise ModuleNotFoundError(msg)
        args.extend(['--timeout', str(int(timeout))])

    # Skip slow tests by default and always skip tooslow tests
    if kwargs.get('slow', False):
        args.extend(['-m', 'slow and not tooslow'])
    else:
        args.extend(['-m', 'not slow and not tooslow'])

    if (split := kwargs.get('split')) is not None:
        if not pytest_plugin_manager.has_split:
            msg = '`pytest-split` plugin required to run tests as groups.'
            raise ModuleNotFoundError(msg)
        match = split_pattern.match(split)
        if not match:
            msg = ('split must be a string of the form a/b where a and b are '
                   'positive nonzero ints')
            raise ValueError(msg)
        group, splits = map(str, match.groups())
        args.extend(['--group', group, '--splits', splits])
        if group > splits:
            msg = (f'cannot have a group number {group} with only {splits} '
                   'splits')
            raise ValueError(msg)

    if blacklist := kwargs.get('blacklist', BLACKLIST_DEFAULT):
        for path in blacklist:
            args.extend(['--ignore', make_absolute_path(path)])

    if kwargs.get('parallel', False):
        if not pytest_plugin_manager.has_xdist:
            msg = '`pytest-xdist` plugin required to run tests in parallel.'
            raise ModuleNotFoundError(msg)
        args.extend(['-n', 'auto'])

    if kwargs.get('store_durations', False):
        if not pytest_plugin_manager.has_split:
            msg = '`pytest-split` plugin required to store test durations.'
            raise ModuleNotFoundError(msg)
        args.append('--store-durations')

    if (keywords := kwargs.get('kw')) is not None:
        keywords = tuple(str(kw) for kw in keywords)
    else:
        keywords = ()

    args = update_args_with_paths(paths, keywords, args)
    exit_code = pytest.main(args)
    return exit_code


def test():
    unittest.main(__name__)


def test():
    """

    Lightweight test for helpers

    """

    r = pygame.Rect(0, 0, 10, 10)
    assert rect_outer_bounds(r) == [(10, 0), (0, 10), (10, 10)]  # tr # bl # br

    assert len(list(rect_area_pts(r))) == 100

    r = pygame.Rect(0, 0, 3, 3)
    assert list(rect_perimeter_pts(r)) == [
        (0, 0),
        (1, 0),
        (2, 0),  # tl -> tr
        (2, 1),
        (2, 2),  # tr -> br
        (1, 2),
        (0, 2),  # br -> bl
        (0, 1),  # bl -> tl
    ]

    print("Tests: OK")


def test(extra_args: list[str] | None = None, run_doctests: bool = False) -> None:  # noqa: PT028
    """
    Run the pandas test suite using pytest.

    By default, runs with the marks -m "not slow and not network and not db"

    Parameters
    ----------
    extra_args : list[str], default None
        Extra marks to run the tests.
    run_doctests : bool, default False
        Whether to only run the Python and Cython doctests. If you would like to run
        both doctests/regular tests, just append "--doctest-modules"/"--doctest-cython"
        to extra_args.

    See Also
    --------
    pytest.main : The main entry point for pytest testing framework.

    Examples
    --------
    >>> pd.test()  # doctest: +SKIP
    running: pytest...
    """
    pytest = import_optional_dependency("pytest")
    import_optional_dependency("hypothesis")
    cmd = ["-m not slow and not network and not db"]
    if extra_args:
        if not isinstance(extra_args, list):
            extra_args = [extra_args]
        cmd = extra_args
    if run_doctests:
        cmd = [
            "--doctest-modules",
            "--doctest-cython",
            f"--ignore={os.path.join(PKG, 'tests')}",
        ]
    cmd += [PKG]
    joined = " ".join(cmd)
    print(f"running: pytest {joined}")
    sys.exit(pytest.main(cmd))


def test(pipeline, batch_size=1, steps=4, control_image=None, warmup_runs=3, test_runs=10, seed=123, verbose=False):
    control_net_args = {}
    if hasattr(pipeline, "controlnet"):
        control_net_args = {
            "image": control_image,
            "controlnet_conditioning_scale": 0.5,
        }

    warmup_prompt = "warm up"
    for _ in range(warmup_runs):
        images = pipeline(
            prompt=warmup_prompt,
            num_inference_steps=steps,
            num_images_per_prompt=batch_size,
            guidance_scale=0.0,
            **control_net_args,
        ).images
        assert len(images) == batch_size

    generator = torch.Generator(device="cuda")
    generator.manual_seed(seed)

    prompt = get_prompt()

    latency_list = []
    images = None
    for _ in range(test_runs):
        torch.cuda.synchronize()
        start_time = time.perf_counter()
        images = pipeline(
            prompt=prompt,
            num_inference_steps=steps,
            num_images_per_prompt=batch_size,
            guidance_scale=0.0,
            generator=generator,
            **control_net_args,
        ).images
        torch.cuda.synchronize()
        seconds = time.perf_counter() - start_time
        latency_list.append(seconds)

    if verbose:
        print(latency_list)

    return images, latency_list


def test():
    np.random.seed(np.arange(10))

    # Create a random array
    ndims = randint(5) + 1
    shape = tuple(randint(10) + 1 for dim in range(ndims))
    els = reduce(mul, shape)
    a = np.arange(els).reshape(shape)

    buf_size = randint(2 * els)
    b = Arrayterator(a, buf_size)

    # Check that each block has at most ``buf_size`` elements
    for block in b:
        assert_(len(block.flat) <= (buf_size or els))

    # Check that all elements are iterated correctly
    assert_(list(b.flat) == list(a.flat))

    # Slice arrayterator
    start = [randint(dim) for dim in shape]
    stop = [randint(dim) + 1 for dim in shape]
    step = [randint(dim) + 1 for dim in shape]
    slice_ = tuple(slice(*t) for t in zip(start, stop, step))
    c = b[slice_]
    d = a[slice_]

    # Check that each block has at most ``buf_size`` elements
    for block in c:
        assert_(len(block.flat) <= (buf_size or els))

    # Check that the arrayterator is sliced correctly
    assert_(np.all(c.__array__() == d))

    # Check that all elements are iterated correctly
    assert_(list(c.flat) == list(d.flat))


def test():
    """
    Tests for :func:`.convertUFO1OrUFO2KerningToUFO3Kerning`.

    No known prefixes.

    >>> testKerning = {
    ...     "A" : {
    ...         "A" : 1,
    ...         "B" : 2,
    ...         "CGroup" : 3,
    ...         "DGroup" : 4
    ...     },
    ...     "BGroup" : {
    ...         "A" : 5,
    ...         "B" : 6,
    ...         "CGroup" : 7,
    ...         "DGroup" : 8
    ...     },
    ...     "CGroup" : {
    ...         "A" : 9,
    ...         "B" : 10,
    ...         "CGroup" : 11,
    ...         "DGroup" : 12
    ...     },
    ... }
    >>> testGroups = {
    ...     "BGroup" : ["B"],
    ...     "CGroup" : ["C"],
    ...     "DGroup" : ["D"],
    ... }
    >>> kerning, groups, maps = convertUFO1OrUFO2KerningToUFO3Kerning(
    ...     testKerning, testGroups, [])
    >>> expected = {
    ...     "A" : {
    ...         "A": 1,
    ...         "B": 2,
    ...         "public.kern2.CGroup": 3,
    ...         "public.kern2.DGroup": 4
    ...     },
    ...     "public.kern1.BGroup": {
    ...         "A": 5,
    ...         "B": 6,
    ...         "public.kern2.CGroup": 7,
    ...         "public.kern2.DGroup": 8
    ...     },
    ...     "public.kern1.CGroup": {
    ...         "A": 9,
    ...         "B": 10,
    ...         "public.kern2.CGroup": 11,
    ...         "public.kern2.DGroup": 12
    ...     }
    ... }
    >>> kerning == expected
    True
    >>> expected = {
    ...     "BGroup": ["B"],
    ...     "CGroup": ["C"],
    ...     "DGroup": ["D"],
    ...     "public.kern1.BGroup": ["B"],
    ...     "public.kern1.CGroup": ["C"],
    ...     "public.kern2.CGroup": ["C"],
    ...     "public.kern2.DGroup": ["D"],
    ... }
    >>> groups == expected
    True

    Known prefixes.

    >>> testKerning = {
    ...     "A" : {
    ...         "A" : 1,
    ...         "B" : 2,
    ...         "@MMK_R_CGroup" : 3,
    ...         "@MMK_R_DGroup" : 4
    ...     },
    ...     "@MMK_L_BGroup" : {
    ...         "A" : 5,
    ...         "B" : 6,
    ...         "@MMK_R_CGroup" : 7,
    ...         "@MMK_R_DGroup" : 8
    ...     },
    ...     "@MMK_L_CGroup" : {
    ...         "A" : 9,
    ...         "B" : 10,
    ...         "@MMK_R_CGroup" : 11,
    ...         "@MMK_R_DGroup" : 12
    ...     },
    ... }
    >>> testGroups = {
    ...     "@MMK_L_BGroup" : ["B"],
    ...     "@MMK_L_CGroup" : ["C"],
    ...     "@MMK_L_XGroup" : ["X"],
    ...     "@MMK_R_CGroup" : ["C"],
    ...     "@MMK_R_DGroup" : ["D"],
    ...     "@MMK_R_XGroup" : ["X"],
    ... }
    >>> kerning, groups, maps = convertUFO1OrUFO2KerningToUFO3Kerning(
    ...     testKerning, testGroups, [])
    >>> expected = {
    ...     "A" : {
    ...         "A": 1,
    ...         "B": 2,
    ...         "public.kern2.CGroup": 3,
    ...         "public.kern2.DGroup": 4
    ...     },
    ...     "public.kern1.BGroup": {
    ...         "A": 5,
    ...         "B": 6,
    ...         "public.kern2.CGroup": 7,
    ...         "public.kern2.DGroup": 8
    ...     },
    ...     "public.kern1.CGroup": {
    ...         "A": 9,
    ...         "B": 10,
    ...         "public.kern2.CGroup": 11,
    ...         "public.kern2.DGroup": 12
    ...     }
    ... }
    >>> kerning == expected
    True
    >>> expected = {
    ...     "@MMK_L_BGroup": ["B"],
    ...     "@MMK_L_CGroup": ["C"],
    ...     "@MMK_L_XGroup": ["X"],
    ...     "@MMK_R_CGroup": ["C"],
    ...     "@MMK_R_DGroup": ["D"],
    ...     "@MMK_R_XGroup": ["X"],
    ...     "public.kern1.BGroup": ["B"],
    ...     "public.kern1.CGroup": ["C"],
    ...     "public.kern1.XGroup": ["X"],
    ...     "public.kern2.CGroup": ["C"],
    ...     "public.kern2.DGroup": ["D"],
    ...     "public.kern2.XGroup": ["X"],
    ... }
    >>> groups == expected
    True

    >>> from .validators import kerningValidator
    >>> kerningValidator(kerning)
    (True, None)

    Mixture of known prefixes and groups without prefixes.

    >>> testKerning = {
    ...     "A" : {
    ...         "A" : 1,
    ...         "B" : 2,
    ...         "@MMK_R_CGroup" : 3,
    ...         "DGroup" : 4
    ...     },
    ...     "BGroup" : {
    ...         "A" : 5,
    ...         "B" : 6,
    ...         "@MMK_R_CGroup" : 7,
    ...         "DGroup" : 8
    ...     },
    ...     "@MMK_L_CGroup" : {
    ...         "A" : 9,
    ...         "B" : 10,
    ...         "@MMK_R_CGroup" : 11,
    ...         "DGroup" : 12
    ...     },
    ... }
    >>> testGroups = {
    ...     "BGroup" : ["B"],
    ...     "@MMK_L_CGroup" : ["C"],
    ...     "@MMK_R_CGroup" : ["C"],
    ...     "DGroup" : ["D"],
    ... }
    >>> kerning, groups, maps = convertUFO1OrUFO2KerningToUFO3Kerning(
    ...     testKerning, testGroups, [])
    >>> expected = {
    ...     "A" : {
    ...         "A": 1,
    ...         "B": 2,
    ...         "public.kern2.CGroup": 3,
    ...         "public.kern2.DGroup": 4
    ...     },
    ...     "public.kern1.BGroup": {
    ...         "A": 5,
    ...         "B": 6,
    ...         "public.kern2.CGroup": 7,
    ...         "public.kern2.DGroup": 8
    ...     },
    ...     "public.kern1.CGroup": {
    ...         "A": 9,
    ...         "B": 10,
    ...         "public.kern2.CGroup": 11,
    ...         "public.kern2.DGroup": 12
    ...     }
    ... }
    >>> kerning == expected
    True
    >>> expected = {
    ...     "BGroup": ["B"],
    ...     "@MMK_L_CGroup": ["C"],
    ...     "@MMK_R_CGroup": ["C"],
    ...     "DGroup": ["D"],
    ...     "public.kern1.BGroup": ["B"],
    ...     "public.kern1.CGroup": ["C"],
    ...     "public.kern2.CGroup": ["C"],
    ...     "public.kern2.DGroup": ["D"],
    ... }
    >>> groups == expected
    True
    """


def test(*args, **kwargs):
    problems = defaultdict(list)
    for glyphname, problem in test_gen(*args, **kwargs):
        problems[glyphname].append(problem)
    return problems

