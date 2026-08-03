from typing import Any, Callable

def collect_cases(fn: Callable[..., Iterator[Case]]) -> Callable[..., None]:
    """run_stubtest used to be slow, so we used this decorator to combine cases.

    If you're reading this and bored, feel free to refactor this and make it more like
    other mypy tests.

    """

    def test(*args: Any, **kwargs: Any) -> None:
        cases = list(fn(*args, **kwargs))
        expected_errors = set()
        for c in cases:
            if c.error is None:
                continue
            expected_error = c.error
            if expected_error == "":
                expected_error = TEST_MODULE_NAME
            elif not expected_error.startswith(f"{TEST_MODULE_NAME}."):
                expected_error = f"{TEST_MODULE_NAME}.{expected_error}"
            assert expected_error not in expected_errors, (
                "collect_cases merges cases into a single stubtest invocation; we already "
                "expect an error for {}".format(expected_error)
            )
            expected_errors.add(expected_error)
        output = run_stubtest(
            stub="\n\n".join(textwrap.dedent(c.stub.lstrip("\n")) for c in cases),
            runtime="\n\n".join(textwrap.dedent(c.runtime.lstrip("\n")) for c in cases),
            options=["--generate-allowlist", "--strict-type-check-only"],
        )

        actual_errors = set(output.splitlines())
        if actual_errors != expected_errors:
            output = run_stubtest(
                stub="\n\n".join(textwrap.dedent(c.stub.lstrip("\n")) for c in cases),
                runtime="\n\n".join(textwrap.dedent(c.runtime.lstrip("\n")) for c in cases),
                options=[],
            )
            assert actual_errors == expected_errors, output

    return test

