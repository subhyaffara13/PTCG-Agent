
def get_vendor_from_model(model: str) -> OCIVendors:
    """Return the OCI vendor enum for a model name.

    OCI GenAI uses two ``apiFormat`` values:

    - ``"COHERE"`` for Cohere models (``cohere.*``)
    - ``"GENERIC"`` for all others (Meta Llama, xAI Grok, Google Gemini, …)
    """
    name = model[4:] if model.lower().startswith("oci/") else model
    vendor = name.split(".")[0].lower()
    if vendor == "cohere":
        return OCIVendors.COHERE
    return OCIVendors.GENERIC

