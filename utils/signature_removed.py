
def signature_removed(nb):
    """Context manager for operating on a notebook with its signature removed

    Used for excluding the previous signature when computing a notebook's signature.
    """
    save_signature = nb["metadata"].pop("signature", None)
    try:
        yield
    finally:
        if save_signature is not None:
            nb["metadata"]["signature"] = save_signature

