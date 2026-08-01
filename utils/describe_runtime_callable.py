
def describe_runtime_callable(signature: inspect.Signature, *, is_async: bool) -> str:
    return f'{"async " if is_async else ""}def {signature}'

