
def make_logging_undefined(
    logger: t.Optional["logging.Logger"] = None, base: t.Type[Undefined] = Undefined
) -> t.Type[Undefined]:
    """Given a logger object this returns a new undefined class that will
    log certain failures.  It will log iterations and printing.  If no
    logger is given a default logger is created.

    Example::

        logger = logging.getLogger(__name__)
        LoggingUndefined = make_logging_undefined(
            logger=logger,
            base=Undefined
        )

    .. versionadded:: 2.8

    :param logger: the logger to use.  If not provided, a default logger
                   is created.
    :param base: the base class to add logging functionality to.  This
                 defaults to :class:`Undefined`.
    """
    if logger is None:
        import logging

        logger = logging.getLogger(__name__)
        logger.addHandler(logging.StreamHandler(sys.stderr))

    def _log_message(undef: Undefined) -> None:
        logger.warning("Template variable warning: %s", undef._undefined_message)

    class LoggingUndefined(base):  # type: ignore
        __slots__ = ()

        def _fail_with_undefined_error(  # type: ignore
            self, *args: t.Any, **kwargs: t.Any
        ) -> "te.NoReturn":
            try:
                super()._fail_with_undefined_error(*args, **kwargs)
            except self._undefined_exception as e:
                logger.error("Template variable error: %s", e)  # type: ignore
                raise e

        def __str__(self) -> str:
            _log_message(self)
            return super().__str__()  # type: ignore

        def __iter__(self) -> t.Iterator[t.Any]:
            _log_message(self)
            return super().__iter__()  # type: ignore

        def __bool__(self) -> bool:
            _log_message(self)
            return super().__bool__()  # type: ignore

    return LoggingUndefined

