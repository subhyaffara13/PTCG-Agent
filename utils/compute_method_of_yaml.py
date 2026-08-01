
def compute_method_of_yaml(variants: set[Variant]) -> list[str]:
    # This is written out explicitly to ensure that Tensor and
    # namespace are put into the list in the right order
    method_of = ["Type"]
    if Variant.method in variants:
        method_of.append("Tensor")
    if Variant.function in variants:
        method_of.append("namespace")
    return method_of

