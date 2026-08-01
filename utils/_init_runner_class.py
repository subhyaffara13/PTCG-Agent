
def _init_runner_class() -> type[doctest.DocTestRunner]:
    import doctest

    class PytestDoctestRunner(doctest.DebugRunner):
        """Runner to collect failures.

        Note that the out variable in this case is a list instead of a
        stdout-like object.
        """

        def __init__(
            self,
            checker: doctest.OutputChecker | None = None,
            verbose: bool | None = None,
            optionflags: int = 0,
            continue_on_failure: bool = True,
        ) -> None:
            super().__init__(checker=checker, verbose=verbose, optionflags=optionflags)
            self.continue_on_failure = continue_on_failure

        def report_failure(
            self,
            out,
            test: doctest.DocTest,
            example: doctest.Example,
            got: str,
        ) -> None:
            failure = doctest.DocTestFailure(test, example, got)
            if self.continue_on_failure:
                out.append(failure)
            else:
                raise failure

        def report_unexpected_exception(
            self,
            out,
            test: doctest.DocTest,
            example: doctest.Example,
            exc_info: tuple[type[BaseException], BaseException, types.TracebackType],
        ) -> None:
            if isinstance(exc_info[1], OutcomeException):
                raise exc_info[1]
            if isinstance(exc_info[1], bdb.BdbQuit):
                outcomes.exit("Quitting debugger")
            failure = doctest.UnexpectedException(test, example, exc_info)
            if self.continue_on_failure:
                out.append(failure)
            else:
                raise failure

    return PytestDoctestRunner

