
def get_flex_attention_lse_kwargs(return_lse: bool) -> dict[str, bool | Optional["AuxRequest"]]:
    """
    Requests the LSE from flex_attention in a version-agnostic fashion.

    Before torch 2.9, the LSE was requested via the boolean return_lse field. However, starting with
    torch 2.9, an AuxRequest object must be passed via the aux_request field. This method conditionally
    returns the correct form based on the python version.
    """
    if _TORCH_FLEX_USE_AUX:
        return {"return_aux": AuxRequest(lse=True) if return_lse else None}

    return {"return_lse": return_lse}

