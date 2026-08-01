
def create_precompile_key(
    name: str, inputs_key: str, choices: list[ChoiceCaller]
) -> str:
    return ":".join(
        [
            name,
            inputs_key,
            torch.get_float32_matmul_precision(),
        ]
        + [choice.kernel_hash_key() for choice in choices]
    )

