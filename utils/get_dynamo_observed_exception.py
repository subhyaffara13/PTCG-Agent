
def get_dynamo_observed_exception(exc_type: type[Exception]) -> type[ObservedException]:
    if exc_type not in observed_exception_map:
        name = getattr(exc_type, "__name__", str(exc_type))
        observed_exception_map[exc_type] = type(  # type: ignore[assignment]
            f"Observed{name}Error", (ObservedException,), {}
        )
    # pyrefly: ignore [bad-index]
    return observed_exception_map[exc_type]

