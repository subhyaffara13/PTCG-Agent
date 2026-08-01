
def is_flash_attention_requested(
    config=None, requested_attention_implementation: str | None = None, version: int | None = None
) -> bool:
    """
    Checks whether some flavor of flash attention is requested or not. Optionally, checks for a specific version of
    flash attention.

    This is checked against one of the two arguments, i.e. either the `config` or the directly passed value
    `requested_attention_implementation`. Otherwise, an error will be raised (ambiguity).

    The different versions of flash attention are usually
    - Implementations based on the original flash attention repo: https://github.com/Dao-AILab/flash-attention
    - Kernels implementations such as: https://huggingface.co/kernels-community/vllm-flash-attn3
    """
    if config is not None and requested_attention_implementation is not None:
        raise ValueError(
            "Requested attention implementation is ambiguous: "
            "Please pass either the config or the name of the attention implementation, not both."
        )

    if config is not None:
        checked_attention_implementation = config._attn_implementation
    else:
        checked_attention_implementation = requested_attention_implementation

    # theoretically can happen, equivalent to default implementation (sdpa/eager)
    if checked_attention_implementation is None:
        return False

    # If a specific version is requested, look for a pattern of type "flash...{version}"
    if version is not None:
        return re.match(r".*flash.*" + str(version), checked_attention_implementation) is not None
    # Otherwise, just check "flash" is in the attention implementation
    return "flash" in checked_attention_implementation

