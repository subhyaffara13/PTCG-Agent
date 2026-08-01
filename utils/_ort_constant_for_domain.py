
def _ort_constant_for_domain(domain: str):
    """
    Map a string domain value to the internal ONNX Runtime constant for that domain.
    :param domain: Domain string to map.
    :return: Internal ONNX Runtime constant
    """

    # constants are defined in <ORT root>/include/onnxruntime/core/graph/constants.h
    # This list is limited to just the domains we have processors for
    domain_to_constant_map = {"ai.onnx": "kOnnxDomain", "ai.onnx.ml": "kMLDomain", "com.microsoft": "kMSDomain"}

    if domain not in domain_to_constant_map:
        raise ValueError(f"Domain {domain} not found in map to ONNX Runtime constant. Please update map.")

    return domain_to_constant_map[domain]

