
def _validate_embed_dim(query: Tensor, key: Tensor, value: Tensor) -> None:
    if query.size(-1) != key.size(-1):
        raise ValueError(
            f"Expect query and key/value to have the same embedding dimension "
            f"but got E={query.size(-1)} and E={key.size(-1)}."
        )

