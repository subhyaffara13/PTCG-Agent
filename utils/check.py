import copy
from typing import Any, Callable

def check(obj, *args, **kwds):
    """
    Check pickling of an object across another process.

    *python* is the path to the python interpreter (defaults to sys.executable)

    Set *verbose=True* to print the unpickled object in the other process.

    Additional keyword arguments are as :func:`dumps` and :func:`loads`.
    """
   # == undocumented ==
   # python -- the string path or executable name of the selected python
   # verbose -- if True, be verbose about printing warning messages
   # all other args and kwds are passed to dill.dumps #FIXME: ignore on load
    verbose = kwds.pop('verbose', False)
    python = kwds.pop('python', None)
    if python is None:
        import sys
        python = sys.executable
    # type check
    isinstance(python, str)
    import subprocess
    fail = True
    try:
        _obj = dumps(obj, *args, **kwds)
        fail = False
    finally:
        if fail and verbose:
            print("DUMP FAILED")
    #FIXME: fails if python interpreter path contains spaces
    # Use the following instead (which also processes the 'ignore' keyword):
    #    ignore = kwds.pop('ignore', None)
    #    unpickle = "dill.loads(%s, ignore=%s)"%(repr(_obj), repr(ignore))
    #    cmd = [python, "-c", "import dill; print(%s)"%unpickle]
    #    msg = "SUCCESS" if not subprocess.call(cmd) else "LOAD FAILED"
    msg = "%s -c import dill; print(dill.loads(%s))" % (python, repr(_obj))
    msg = "SUCCESS" if not subprocess.call(msg.split(None,2)) else "LOAD FAILED"
    if verbose:
        print(msg)
    return


def check(feature: str) -> bool | None:
    """
    :param feature: A module, codec, or feature name.
    :returns:
        ``True`` if the module, codec, or feature is available,
        ``False`` or ``None`` otherwise.
    """

    if feature in modules:
        return check_module(feature)
    if feature in codecs:
        return check_codec(feature)
    if feature in features:
        return check_feature(feature)
    warnings.warn(f"Unknown feature '{feature}'.", stacklevel=2)
    return False


def check(codeString, filename, reporter=None):
    """
    Check the Python source given by C{codeString} for flakes.

    @param codeString: The Python source to check.
    @type codeString: C{str}

    @param filename: The name of the file the source came from, used to report
        errors.
    @type filename: C{str}

    @param reporter: A L{Reporter} instance, where errors and warnings will be
        reported.

    @return: The number of warnings emitted.
    @rtype: C{int}
    """
    if reporter is None:
        reporter = modReporter._makeDefaultReporter()
    # First, compile into an AST and handle syntax errors.
    try:
        tree = ast.parse(codeString, filename=filename)
    except SyntaxError as e:
        reporter.syntaxError(filename, e.args[0], e.lineno, e.offset, e.text)
        return 1
    except Exception:
        reporter.unexpectedError(filename, 'problem decoding source')
        return 1
    # Okay, it's syntactically valid.  Now check it.
    w = checker.Checker(tree, filename=filename)
    w.messages.sort(key=lambda m: m.lineno)
    for warning in w.messages:
        reporter.flake(warning)
    return len(w.messages)


def check(cond, msg):
    if not cond:
        raise ValueError(msg)


def check(obj: Any, is_inlined_call: bool = False, frame: Any | None = None) -> bool:
    return check_verbose(obj, is_inlined_call, frame).skipped


def check(
    b: bool, s: Callable[[], str], exc_type: type[Exception] = RuntimeError
) -> None:
    """
    Helper function for raising an error_type (default: RuntimeError) if a boolean condition fails.
    Error message is a callable producing a string (to avoid wasting time
    string formatting in non-error case, and also to make it easier for torchdynamo
    to trace.)

    .. note:: This function is planned for removal in the future. Please use
        `torch._check*` functions instead.
    """
    torch._check_with(exc_type, b, s)


def check(commit: _Commit, force_unsafe: bool = False):
    next_version = None
    reason = ""
    # Step 1: Detect major schema updates.
    if len(commit.additions) > 0:
        for k, v in commit.additions.items():
            if k not in commit.base:
                continue
            kind = commit.result[k]["kind"]
            fields = v["fields"]
            for f, d in fields.items():
                if kind == "struct" and "default" not in d:
                    reason += (
                        f"Field {k}.{f} is added to schema.py without a default value as an incompatible change "
                        + "which requires major version bump.\n"
                    )
                    next_version = [commit.base["SCHEMA_VERSION"][0] + 1, 1]

    if len(commit.subtractions) > 0:
        for k, v in commit.subtractions.items():
            if k not in commit.result:
                continue
            for f in v["fields"]:
                reason = f"Field {k}.{f} is removed from schema.py as an incompatible change which requires major version bump.\n"
            next_version = [commit.base["SCHEMA_VERSION"][0] + 1, 1]

    if force_unsafe:
        reason += "--force-unsafe is used."
        next_version = commit.result["SCHEMA_VERSION"]
    else:
        # Step 2: Detect minor schema updates.
        if next_version is None and len(commit.additions) > 0:
            for k, v in commit.additions.items():
                for f in v["fields"]:
                    reason += (
                        f"Field {k}.{f} is added to schema.py as an compatible change "
                        + "which still requires minor version bump.\n"
                    )
            next_version = [
                commit.base["SCHEMA_VERSION"][0],
                commit.base["SCHEMA_VERSION"][1] + 1,
            ]
        if next_version is None and len(commit.subtractions) > 0:
            for k, v in commit.subtractions.items():
                for f in v["fields"]:
                    reason += (
                        f"Field {k}.{f} is removed from schema.py as an compatible change "
                        + "which still requires minor version bump.\n"
                    )
            next_version = [
                commit.base["SCHEMA_VERSION"][0],
                commit.base["SCHEMA_VERSION"][1] + 1,
            ]

    return next_version, reason


def check(a, exclude=[], check_attr=True, deprecated=()):
    """ Check that pickling and copying round-trips.
    """
    # Pickling with protocols 0 and 1 is disabled for Basic instances:
    if isinstance(a, Basic):
        for protocol in [0, 1]:
            raises(NotImplementedError, lambda: pickle.dumps(a, protocol))

    protocols = [2, copy.copy, copy.deepcopy, 3, 4]
    if cloudpickle:
        protocols.extend([cloudpickle])

    for protocol in protocols:
        if protocol in exclude:
            continue

        if callable(protocol):
            if isinstance(a, type):
                # Classes can't be copied, but that's okay.
                continue
            b = protocol(a)
        elif inspect.ismodule(protocol):
            b = protocol.loads(protocol.dumps(a))
        else:
            b = pickle.loads(pickle.dumps(a, protocol))

        d1 = dir(a)
        d2 = dir(b)
        assert set(d1) == set(d2)

        if not check_attr:
            continue

        def c(a, b, d):
            for i in d:
                if i in dont_check_attrs:
                    continue
                elif i in not_equal_attrs:
                    if hasattr(a, i):
                        assert hasattr(b, i), i
                elif i in deprecated_attrs or i in deprecated:
                    with ignore_warnings(SymPyDeprecationWarning):
                        assert getattr(a, i) == getattr(b, i), i
                elif not hasattr(a, i):
                    continue
                else:
                    attr = getattr(a, i)
                    if not hasattr(attr, "__call__"):
                        assert hasattr(b, i), i
                        assert getattr(b, i) == attr, "%s != %s, protocol: %s" % (getattr(b, i), attr, protocol)

        c(a, b, d1)
        c(b, a, d2)


def check(name, func, z, y):
    global errcount
    try:
        x = func(z)
    except:
        errcount += 1
        if raise_:
            raise
        print()
        print(name)
        print("EXCEPTION")
        import traceback
        traceback.print_tb(sys.exc_info()[2])
        print()
        return
    xre = x.real
    xim = x.imag
    yre = y.real
    yim = y.imag
    tol = eps*8
    err = 0
    if abs(xre-yre) > abs(yre)*tol:
        err = 1
        print()
        print("Error! %s (re = %s, wanted %s, err=%s)" % (name, nstr(xre,10), nstr(yre,10), nstr(abs(xre-yre))))
        errcount += 1
        if raise_:
            raise SystemExit
    if abs(xim-yim) > abs(yim)*tol:
        err = 1
        print()
        print("Error! %s (im = %s, wanted %s, err=%s)" % (name, nstr(xim,10), nstr(yim,10), nstr(abs(xim-yim))))
        errcount += 1
        if raise_:
            raise SystemExit
    if not err:
        sys.stdout.write("%s ok; " % name)


def check(pred: Bool, msg: str,
          *fmt_args,
          debug: bool = False,
          **fmt_kwargs,
          ) -> None:
  """Check a predicate, add an error with msg if predicate is False.

  This is an effectful operation, and can't be staged (jitted/scanned/...).
  Before staging a function with checks, :func:`~checkify` it!

  Args:
    pred: if False, a FailedCheckError error is added.
    msg: error message if error is added. Can be a format string.
    debug: Whether to turn on debugging mode. If True, check will be removed
      during execution. If False, the check must be functionalized using
      checkify.checkify.
    fmt_args, fmt_kwargs: Positional and keyword formatting arguments for
      `msg`, eg.:
      ``check(.., "check failed on values {} and {named_arg}", x, named_arg=y)``
      Note that these arguments can be traced values allowing you to add
      run-time values to the error message.
      Note that tracking these run-time arrays will increase your memory usage,
      even if no error happens.

  For example:

    >>> import jax
    >>> import jax.numpy as jnp
    >>> from jax.experimental import checkify
    >>> def f(x):
    ...   checkify.check(x>0, "{x} needs to be positive!", x=x)
    ...   return 1/x
    >>> checked_f = checkify.checkify(f)
    >>> err, out = jax.jit(checked_f)(-3.)
    >>> err.throw()  # doctest: +IGNORE_EXCEPTION_DETAIL
    Traceback (most recent call last):
      ...
    jax._src.checkify.JaxRuntimeError: -3. needs to be positive!

  """
  _check(pred, msg, debug, *fmt_args, **fmt_kwargs)


def check(d, ok=True):
    res = []
    for k,v in d.items():
        try:
            z = dill.copy(v)
            if ok: res.append(k)
        except:
            if not ok: res.append(k)
    return res

