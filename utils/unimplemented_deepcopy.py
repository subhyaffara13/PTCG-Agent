
def unimplemented_deepcopy(*args: Any, **kwargs: Any) -> NoReturn:
    raise AssertionError(
        "DDP does not support deepcopy. Please use state dict for serialization."
    )

