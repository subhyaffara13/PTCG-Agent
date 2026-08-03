import sys

def _postmortem_exc_or_tb(
    excinfo: ExceptionInfo[BaseException],
) -> types.TracebackType | BaseException:
    from doctest import UnexpectedException

    get_exc = sys.version_info >= (3, 13)
    if isinstance(excinfo.value, UnexpectedException):
        # A doctest.UnexpectedException is not useful for post_mortem.
        # Use the underlying exception instead:
        underlying_exc = excinfo.value
        if get_exc:
            return underlying_exc.exc_info[1]

        return underlying_exc.exc_info[2]
    elif isinstance(excinfo.value, ConftestImportFailure):
        # A config.ConftestImportFailure is not useful for post_mortem.
        # Use the underlying exception instead:
        cause = excinfo.value.cause
        if get_exc:
            return cause

        assert cause.__traceback__ is not None
        return cause.__traceback__
    else:
        assert excinfo._excinfo is not None
        if get_exc:
            return excinfo._excinfo[1]

        return excinfo._excinfo[2]

