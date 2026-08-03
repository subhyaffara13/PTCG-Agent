import functools

def _deprecate_positional_args(func=None, *, version=None,
                               deprecated_args=None, custom_message=""):
    """Decorator for methods that issues warnings for positional arguments.

    Using the keyword-only argument syntax in pep 3102, arguments after the
    * will issue a warning when passed as a positional argument.

    Parameters
    ----------
    func : callable, default=None
        Function to check arguments on.
    version : callable, default=None
        The version when positional arguments will result in error.
    deprecated_args : set of str, optional
        Arguments to deprecate - whether passed by position or keyword.
    custom_message : str, optional
        Custom message to add to deprecation warning and documentation.
    """
    if version is None:
        msg = "Need to specify a version where signature will be changed"
        raise ValueError(msg)

    deprecated_args = set() if deprecated_args is None else set(deprecated_args)

    def _inner_deprecate_positional_args(f):
        sig = signature(f)
        kwonly_args = []
        all_args = []

        for name, param in sig.parameters.items():
            if param.kind == Parameter.POSITIONAL_OR_KEYWORD:
                all_args.append(name)
            elif param.kind == Parameter.KEYWORD_ONLY:
                kwonly_args.append(name)

        def warn_deprecated_args(kwargs):
            intersection = deprecated_args.intersection(kwargs)
            if intersection:
                message = (f"Arguments {intersection} are deprecated, whether passed "
                           "by position or keyword. They will be removed in SciPy "
                           f"{version}. ")
                message += custom_message
                warnings.warn(message, category=DeprecationWarning, stacklevel=3)

        @functools.wraps(f)
        def inner_f(*args, **kwargs):

            extra_args = len(args) - len(all_args)
            if extra_args <= 0:
                warn_deprecated_args(kwargs)
                return f(*args, **kwargs)

            # extra_args > 0
            kwonly_extra_args = set(kwonly_args[:extra_args]) - deprecated_args
            args_msg = ", ".join(kwonly_extra_args)
            warnings.warn(
                (
                    f"You are passing as positional arguments: {args_msg}. "
                    "Please change your invocation to use keyword arguments. "
                    f"From SciPy {version}, passing these as positional "
                    "arguments will result in an error."
                ),
                DeprecationWarning,
                stacklevel=2,
            )
            kwargs.update(zip(sig.parameters, args))
            warn_deprecated_args(kwargs)
            return f(**kwargs)

        doc = FunctionDoc(inner_f)
        kwonly_extra_args = set(kwonly_args) - deprecated_args
        admonition = f"""
.. deprecated:: {version}
    Use of argument(s) ``{kwonly_extra_args}`` by position is deprecated; beginning in 
    SciPy {version}, these will be keyword-only. """
        if deprecated_args:
            admonition += (f"Argument(s) ``{deprecated_args}`` are deprecated, whether "
                           "passed by position or keyword; they will be removed in "
                           f"SciPy {version}. ")
        admonition += custom_message
        doc['Extended Summary'] += [admonition]

        doc = str(doc).split("\n", 1)[1].lstrip(" \n")  # remove signature
        inner_f.__doc__ = str(doc)

        return inner_f

    if func is not None:
        return _inner_deprecate_positional_args(func)

    return _inner_deprecate_positional_args


def _deprecate_positional_args(*, version: str):
    """Decorator for methods that issues warnings for positional arguments.
    Using the keyword-only argument syntax in pep 3102, arguments after the
    * will issue a warning when passed as a positional argument.

    Args:
        version (`str`):
            The version when positional arguments will result in error.
    """

    def _inner_deprecate_positional_args(f):
        sig = signature(f)
        kwonly_args = []
        all_args = []
        for name, param in sig.parameters.items():
            if param.kind == Parameter.POSITIONAL_OR_KEYWORD:
                all_args.append(name)
            elif param.kind == Parameter.KEYWORD_ONLY:
                kwonly_args.append(name)

        @wraps(f)
        def inner_f(*args, **kwargs):
            extra_args = len(args) - len(all_args)
            if extra_args <= 0:
                return f(*args, **kwargs)
            # extra_args > 0
            args_msg = [
                f"{name}='{arg}'" if isinstance(arg, str) else f"{name}={arg}"
                for name, arg in zip(kwonly_args[:extra_args], args[-extra_args:])
            ]
            args_msg = ", ".join(args_msg)
            warnings.warn(
                f"Deprecated positional argument(s) used in '{f.__name__}': pass"
                f" {args_msg} as keyword args. From version {version} passing these"
                " as positional arguments will result in an error,",
                FutureWarning,
            )
            kwargs.update(zip(sig.parameters, args))
            return f(**kwargs)

        return inner_f

    return _inner_deprecate_positional_args

