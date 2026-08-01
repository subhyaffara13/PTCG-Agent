
def _eval_scope_callable(
    scope_callable: Callable[[str, Config], ScopeName],
    fixture_name: str,
    config: Config,
) -> ScopeName:
    try:
        # Type ignored because there is no typing mechanism to specify
        # keyword arguments, currently.
        result = scope_callable(fixture_name=fixture_name, config=config)  # type: ignore[call-arg]
    except Exception as e:
        raise TypeError(
            f"Error evaluating {scope_callable} while defining fixture '{fixture_name}'.\n"
            "Expected a function with the signature (*, fixture_name, config)"
        ) from e
    if not isinstance(result, str):
        fail(
            f"Expected {scope_callable} to return a 'str' while defining fixture '{fixture_name}', but it returned:\n"
            f"{result!r}",
            pytrace=False,
        )
    return result

