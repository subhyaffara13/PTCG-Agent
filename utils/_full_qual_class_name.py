
def _full_qual_class_name(qualname: str) -> str:
    ns, name = parse_namespace(qualname)
    return "__torch__.torch.classes." + ns + "." + name

