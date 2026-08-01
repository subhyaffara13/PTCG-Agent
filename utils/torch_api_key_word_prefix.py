
def torch_api_key_word_prefix(bankend_index: BackendIndex) -> str:
    if bankend_index.external:
        return ""

    # Although Intel GPU ATen library is out-of-tree, it still utilizes torchgen to produce structured
    # kernels. Regarding these produced structured kernels, they should be visible for the Intel GPU ATen
    # library. Therefore, we need to add "TORCH_XPU_API" prefix to these structured kernels,
    # rather than "TORCH_API". Because the semantic of "TORCH_API" is "hidden" for out-of-tree backends.
    # For other in-tree backends like cpu and cuda, they still use "TORCH_API" prefix with "visible" semantic.
    device_torch_api_key_word_mapping = {
        "XPU": "TORCH_XPU_API",
    }

    return (
        device_torch_api_key_word_mapping.get(
            bankend_index.dispatch_key.name, "TORCH_API"
        )
        + " "
    )

