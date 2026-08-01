
def deprecated(
    value: object,
    module_name: str,
    message: str,
    warning_class: type[Warning],
    name: str | None = None,
) -> _DeprecatedValue:
    module = sys.modules[module_name]
    if not isinstance(module, _ModuleWithDeprecations):
        sys.modules[module_name] = module = _ModuleWithDeprecations(module)
    dv = _DeprecatedValue(value, message, warning_class)
    # Maintain backwards compatibility with `name is None` for pyOpenSSL.
    if name is not None:
        setattr(module, name, dv)
    return dv


def deprecated():
    """
    When we deprecate a function that might still be in use, we make it internal
    by adding a leading underscore. This decorator is used with a private function,
    and creates a public alias without the leading underscore, but has a deprecation
    warning. This tells users "THIS FUNCTION IS DEPRECATED, please use something else"
    without breaking them, however, if they still really really want to use the
    deprecated function without the warning, they can do so by using the internal
    function name.
    """

    def decorator(func: Callable[_P, _T]) -> Callable[_P, _T]:
        # Validate naming convention - single leading underscore, not dunder
        if not (func.__name__.startswith("_")):
            raise ValueError(
                "@deprecate must decorate a function whose name "
                "starts with a single leading underscore (e.g. '_foo') as the api should be considered internal for deprecation."
            )

        public_name = func.__name__[1:]  # drop exactly one leading underscore
        module = sys.modules[func.__module__]

        # Don't clobber an existing symbol accidentally.
        if hasattr(module, public_name):
            raise RuntimeError(
                f"Cannot create alias '{public_name}' -> symbol already exists in {module.__name__}. \
                 Please rename it or consult a pytorch developer on what to do"
            )

        warning_msg = f"{func.__name__[1:]} is DEPRECATED, please consider using an alternative API(s). "

        # public deprecated alias
        alias = typing_extensions.deprecated(
            # pyrefly: ignore [bad-argument-type]
            warning_msg,
            category=UserWarning,
            stacklevel=1,
        )(func)

        alias.__name__ = public_name

        # Adjust qualname if nested inside a class or another function
        if "." in func.__qualname__:
            alias.__qualname__ = func.__qualname__.rsplit(".", 1)[0] + "." + public_name
        else:
            alias.__qualname__ = public_name

        setattr(module, public_name, alias)

        return func

    return decorator


def deprecated(message, *, deprecated_since_version,
               active_deprecations_target, stacklevel=3):
    '''
    Mark a function as deprecated.

    This decorator should be used if an entire function or class is
    deprecated. If only a certain functionality is deprecated, you should use
    :func:`~.warns_deprecated_sympy` directly. This decorator is just a
    convenience. There is no functional difference between using this
    decorator and calling ``warns_deprecated_sympy()`` at the top of the
    function.

    The decorator takes the same arguments as
    :func:`~.warns_deprecated_sympy`. See its
    documentation for details on what the keywords to this decorator do.

    See the :ref:`deprecation-policy` document for details on when and how
    things should be deprecated in SymPy.

    Examples
    ========

    >>> from sympy.utilities.decorator import deprecated
    >>> from sympy import simplify
    >>> @deprecated("""\
    ... The simplify_this(expr) function is deprecated. Use simplify(expr)
    ... instead.""", deprecated_since_version="1.1",
    ... active_deprecations_target='simplify-this-deprecation')
    ... def simplify_this(expr):
    ...     """
    ...     Simplify ``expr``.
    ...
    ...     .. deprecated:: 1.1
    ...
    ...        The ``simplify_this`` function is deprecated. Use :func:`simplify`
    ...        instead. See its documentation for more information. See
    ...        :ref:`simplify-this-deprecation` for details.
    ...
    ...     """
    ...     return simplify(expr)
    >>> from sympy.abc import x
    >>> simplify_this(x*(x + 1) - x**2) # doctest: +SKIP
    <stdin>:1: SymPyDeprecationWarning:
    <BLANKLINE>
    The simplify_this(expr) function is deprecated. Use simplify(expr)
    instead.
    <BLANKLINE>
    See https://docs.sympy.org/latest/explanation/active-deprecations.html#simplify-this-deprecation
    for details.
    <BLANKLINE>
    This has been deprecated since SymPy version 1.1. It
    will be removed in a future version of SymPy.
    <BLANKLINE>
      simplify_this(x)
    x

    See Also
    ========
    sympy.utilities.exceptions.SymPyDeprecationWarning
    sympy.utilities.exceptions.sympy_deprecation_warning
    sympy.utilities.exceptions.ignore_warnings
    sympy.testing.pytest.warns_deprecated_sympy

    '''
    decorator_kwargs = {"deprecated_since_version": deprecated_since_version,
               "active_deprecations_target": active_deprecations_target}
    def deprecated_decorator(wrapped):
        if hasattr(wrapped, '__mro__'):  # wrapped is actually a class
            class wrapper(wrapped):
                __doc__ = wrapped.__doc__
                __module__ = wrapped.__module__
                _sympy_deprecated_func = wrapped
                if '__new__' in wrapped.__dict__:
                    def __new__(cls, *args, **kwargs):
                        sympy_deprecation_warning(message, **decorator_kwargs, stacklevel=stacklevel)
                        return super().__new__(cls, *args, **kwargs)
                else:
                    def __init__(self, *args, **kwargs):
                        sympy_deprecation_warning(message, **decorator_kwargs, stacklevel=stacklevel)
                        super().__init__(*args, **kwargs)
            wrapper.__name__ = wrapped.__name__
        else:
            @wraps(wrapped)
            def wrapper(*args, **kwargs):
                sympy_deprecation_warning(message, **decorator_kwargs, stacklevel=stacklevel)
                return wrapped(*args, **kwargs)
            wrapper._sympy_deprecated_func = wrapped
        return wrapper
    return deprecated_decorator


def deprecated(
    *,
    reason: str,
    replacement: str | None,
    gone_in: str | None,
    feature_flag: str | None = None,
    issue: int | None = None,
    stacklevel: int = 2,
    include_source: bool = False,
) -> None:
    """Helper to deprecate existing functionality.

    reason:
        Textual reason shown to the user about why this functionality has
        been deprecated. Should be a complete sentence.
    replacement:
        Textual suggestion shown to the user about what alternative
        functionality they can use.
    gone_in:
        The version of pip does this functionality should get removed in.
        Raises an error if pip's current version is greater than or equal to
        this.
    feature_flag:
        Command-line flag of the form --use-feature={feature_flag} for testing
        upcoming functionality.
    issue:
        Issue number on the tracker that would serve as a useful place for
        users to find related discussion and provide feedback.
    stacklevel:
        How many frames up the call stack to attribute the warning to.
        Defaults to 2 (the caller of deprecated()).
    include_source:
        If True, include the source filename and line number in the warning
        output. Useful when the warning originates from external code.
    """

    # Determine whether or not the feature is already gone in this version.
    is_gone = gone_in is not None and parse(current_version) >= parse(gone_in)

    message_parts = [
        (reason, f"{DEPRECATION_MSG_PREFIX}{{}}"),
        (
            gone_in,
            (
                "pip {} will enforce this behaviour change."
                if not is_gone
                else "Since pip {}, this is no longer supported."
            ),
        ),
        (
            replacement,
            "A possible replacement is {}.",
        ),
        (
            feature_flag,
            (
                "You can use the flag --use-feature={} to test the upcoming behaviour."
                if not is_gone
                else None
            ),
        ),
        (
            issue,
            "Discussion can be found at https://github.com/pypa/pip/issues/{}",
        ),
    ]

    message = " ".join(
        format_str.format(value)
        for value, format_str in message_parts
        if format_str is not None and value is not None
    )

    # Raise as an error if this behaviour is deprecated.
    if is_gone:
        raise PipDeprecationWarning(message)

    warning = PipDeprecationWarning(message)
    warning.include_source = include_source
    warnings.warn(warning, stacklevel=stacklevel)


def deprecated(since, *, message='', name='', alternative='', pending=False,
               obj_type=None, addendum='', removal=''):
    """
    Decorator to mark a function, a class, or a property as deprecated.

    When deprecating a classmethod, a staticmethod, or a property, the
    ``@deprecated`` decorator should go *under* ``@classmethod`` and
    ``@staticmethod`` (i.e., `deprecated` should directly decorate the
    underlying callable), but *over* ``@property``.

    When deprecating a class ``C`` intended to be used as a base class in a
    multiple inheritance hierarchy, ``C`` *must* define an ``__init__`` method
    (if ``C`` instead inherited its ``__init__`` from its own base class, then
    ``@deprecated`` would mess up ``__init__`` inheritance when installing its
    own (deprecation-emitting) ``C.__init__``).

    Parameters are the same as for `warn_deprecated`, except that *obj_type*
    defaults to 'class' if decorating a class, 'attribute' if decorating a
    property, and 'function' otherwise.

    Examples
    --------
    ::

        @deprecated('1.4.0')
        def the_function_to_deprecate():
            pass
    """

    def deprecate(obj, message=message, name=name, alternative=alternative,
                  pending=pending, obj_type=obj_type, addendum=addendum):
        from matplotlib._api import classproperty

        if isinstance(obj, type):
            if obj_type is None:
                obj_type = "class"
            func = obj.__init__
            name = name or obj.__name__
            old_doc = obj.__doc__

            def finalize(wrapper, new_doc):
                try:
                    obj.__doc__ = new_doc
                except AttributeError:  # Can't set on some extension objects.
                    pass
                obj.__init__ = functools.wraps(obj.__init__)(wrapper)
                return obj

        elif isinstance(obj, (property, classproperty)):
            if obj_type is None:
                obj_type = "attribute"
            func = None
            name = name or obj.fget.__name__
            old_doc = obj.__doc__

            class _deprecated_property(type(obj)):
                def __get__(self, instance, owner=None):
                    if instance is not None or owner is not None \
                            and isinstance(self, classproperty):
                        emit_warning()
                    return super().__get__(instance, owner)

                def __set__(self, instance, value):
                    if instance is not None:
                        emit_warning()
                    return super().__set__(instance, value)

                def __delete__(self, instance):
                    if instance is not None:
                        emit_warning()
                    return super().__delete__(instance)

                def __set_name__(self, owner, set_name):
                    nonlocal name
                    if name == "<lambda>":
                        name = set_name

            def finalize(_, new_doc):
                return _deprecated_property(
                    fget=obj.fget, fset=obj.fset, fdel=obj.fdel, doc=new_doc)

        else:
            if obj_type is None:
                obj_type = "function"
            func = obj
            name = name or obj.__name__
            old_doc = func.__doc__

            def finalize(wrapper, new_doc):
                wrapper = functools.wraps(func)(wrapper)
                wrapper.__doc__ = new_doc
                return wrapper

        def emit_warning():
            warn_deprecated(
                since, message=message, name=name, alternative=alternative,
                pending=pending, obj_type=obj_type, addendum=addendum,
                removal=removal)

        def wrapper(*args, **kwargs):
            __tracebackhide__ = True
            emit_warning()
            return func(*args, **kwargs)

        old_doc = inspect.cleandoc(old_doc or '').strip('\n')

        notes_header = '\nNotes\n-----'
        second_arg = ' '.join([t.strip() for t in
                               (message, f"Use {alternative} instead."
                                if alternative else "", addendum) if t])
        new_doc = (f"[*Deprecated*] {old_doc}\n"
                   f"{notes_header if notes_header not in old_doc else ''}\n"
                   f".. deprecated:: {since}\n"
                   f"   {second_arg}")

        if not old_doc:
            # This is to prevent a spurious 'unexpected unindent' warning from
            # docutils when the original docstring was blank.
            new_doc += r'\ '

        return finalize(wrapper, new_doc)

    return deprecate


def deprecated(msg: str = "") -> Callable[[F], F]:
    """Decorator factory to mark functions as deprecated with given message.

    >>> @deprecated("Enough!")
    ... def some_function():
    ...    "I just print 'hello world'."
    ...    print("hello world")
    >>> some_function()
    hello world
    >>> some_function.__doc__ == "I just print 'hello world'."
    True
    """

    def deprecated_decorator(func: F) -> F:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            warnings.warn(
                f"{func.__name__} function is a deprecated. {msg}",
                category=DeprecationWarning,
                stacklevel=2,
            )
            return func(*args, **kwargs)

        return cast(F, wrapper)

    return deprecated_decorator


def deprecated(new_fn: F) -> F:
  """Creates a deprecated alias for a renamed function.

  .. deprecated::
     This decorator is for marking functions as deprecated. The returned
     wrapper emits a :class:`DeprecationWarning` on every call and then
     delegates to ``new_fn``.

  The returned callable copies the signature, type annotations, and
  docstring of ``new_fn``, with a deprecation notice prepended to the
  docstring. This keeps IDE autocomplete and type-checking working while
  clearly communicating that callers should migrate.

  Args:
    new_fn: The current, non-deprecated function to delegate to.

  Returns:
    A wrapper that emits a :class:`DeprecationWarning` and then calls
    ``new_fn`` with the same arguments.

  Example::

    >>> from flax.nnx.deprecations import deprecated
    >>> def new_api(x):
    ...   return x * 2
    >>> old_api = deprecated(new_api)

  """

  @functools.wraps(new_fn)
  def wrapper(*args, **kwargs):
    warnings.warn(
      f'This function is deprecated. Use {new_fn.__qualname__} instead.',
      DeprecationWarning,
      stacklevel=2,
    )
    return new_fn(*args, **kwargs)

  dep_notice = (
    f'.. deprecated::\n'
    f'   Use :func:`{new_fn.__qualname__}` instead.\n\n'
  )
  wrapper.__doc__ = dep_notice + (new_fn.__doc__ or '')

  return wrapper  # type: ignore[return-value]

