
def _nonzero_schemas() -> list[inspect.Signature]:
    signatures = []

    def nonzero(self: torch.Tensor) -> None:
        pass

    signatures.append(inspect.signature(nonzero))

    def nonzero(self: torch.Tensor, *, as_tuple: bool) -> None:  # type: ignore[no-redef]
        pass

    signatures.append(inspect.signature(nonzero))

    return signatures

