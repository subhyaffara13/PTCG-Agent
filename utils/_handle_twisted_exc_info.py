import sys

def _handle_twisted_exc_info(
    rawexcinfo: _SysExcInfoType | BaseException,
) -> _SysExcInfoType:
    """
    Twisted passes a custom Failure instance to `addError()` instead of using `sys.exc_info()`.
    Therefore, if `rawexcinfo` is a `Failure` instance, convert it into the equivalent `sys.exc_info()` tuple
    as expected by pytest.
    """
    twisted_version = _get_twisted_version()
    if twisted_version is TwistedVersion.NotInstalled:
        # Unfortunately, because we cannot import `twisted.python.failure` at the top of the file
        # and use it in the signature, we need to use `type:ignore` here because we cannot narrow
        # the type properly in the `if` statement above.
        return rawexcinfo  # type:ignore[return-value]
    elif twisted_version is TwistedVersion.Version24:
        # Twisted calls addError() passing its own classes (like `twisted.python.Failure`), which violates
        # the `addError()` signature, so we extract the original `sys.exc_info()` tuple which is stored
        # in the object.
        if hasattr(rawexcinfo, TWISTED_RAW_EXCINFO_ATTR):
            saved_exc_info = getattr(rawexcinfo, TWISTED_RAW_EXCINFO_ATTR)
            # Delete the attribute from the original object to avoid leaks.
            delattr(rawexcinfo, TWISTED_RAW_EXCINFO_ATTR)
            return saved_exc_info  # type:ignore[no-any-return]
        return rawexcinfo  # type:ignore[return-value]
    elif twisted_version is TwistedVersion.Version25:
        if isinstance(rawexcinfo, BaseException):
            import twisted.python.failure

            if isinstance(rawexcinfo, twisted.python.failure.Failure):
                tb = rawexcinfo.__traceback__
                if tb is None:
                    tb = sys.exc_info()[2]
                return type(rawexcinfo.value), rawexcinfo.value, tb

        return rawexcinfo  # type:ignore[return-value]
    else:
        # Ideally we would use assert_never() here, but it is not available in all Python versions
        # we support, plus we do not require `type_extensions` currently.
        assert False, f"Unexpected Twisted version: {twisted_version}"

