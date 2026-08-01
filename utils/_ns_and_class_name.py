
def _ns_and_class_name(full_qualname: str) -> tuple[str, str]:
    splits = full_qualname.split(".")
    if len(splits) != 5:
        raise AssertionError(f"Could not split {full_qualname=}, expected 5 parts")
    _torch, _torch_ns, _classes, ns, class_name = splits
    return ns, class_name

