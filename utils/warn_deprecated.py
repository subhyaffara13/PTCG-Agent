
def warn_deprecated(name, reason="", version="", stacklevel=2):
    import warnings

    msg = f"Call to deprecated {name}."
    if reason:
        msg += f" ({reason})"
    if version:
        msg += f" -- Deprecated since version {version}."
    warnings.warn(msg, category=DeprecationWarning, stacklevel=stacklevel)


def warn_deprecated():
    warnings.warn(
        "torch._custom_op is deprecated and will be removed in PyTorch 2.6, please "
        "use the equivalent torch.library API instead.",
        DeprecationWarning,
        stacklevel=2,
    )


def warn_deprecated(api: str, new_api: str | None = None) -> None:
    warning = get_warning(api, new_api, replace_newlines=True)
    warnings.warn(warning, FutureWarning, stacklevel=3)


def warn_deprecated(
        since, *, message='', name='', alternative='', pending=False,
        obj_type='', addendum='', removal=''):
    """
    Display a standardized deprecation.

    Parameters
    ----------
    since : str
        The release at which this API became deprecated.
    message : str, optional
        Override the default deprecation message.  The ``%(since)s``,
        ``%(name)s``, ``%(alternative)s``, ``%(obj_type)s``, ``%(addendum)s``,
        and ``%(removal)s`` format specifiers will be replaced by the values
        of the respective arguments passed to this function.
    name : str, optional
        The name of the deprecated object.
    alternative : str, optional
        An alternative API that the user may use in place of the deprecated
        API.  The deprecation warning will tell the user about this alternative
        if provided.
    pending : bool, optional
        If True, uses a PendingDeprecationWarning instead of a
        DeprecationWarning.  Cannot be used together with *removal*.
    obj_type : str, optional
        The object type being deprecated.
    addendum : str, optional
        Additional text appended directly to the final message.
    removal : str, optional
        The expected removal version.  With the default (an empty string), a
        removal version is automatically computed from *since*.  Set to other
        Falsy values to not schedule a removal date.  Cannot be used together
        with *pending*.

    Examples
    --------
    ::

        # To warn of the deprecation of "matplotlib.name_of_module"
        warn_deprecated('1.4.0', name='matplotlib.name_of_module',
                        obj_type='module')
    """
    warning = _generate_deprecation_warning(
        since, message, name, alternative, pending, obj_type, addendum,
        removal=removal)
    from . import warn_external
    warn_external(warning, category=MatplotlibDeprecationWarning)

