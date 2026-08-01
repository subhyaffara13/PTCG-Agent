
def _build_proxy_class(cls_name: str, builtins: nodes.Module) -> nodes.ClassDef:
    proxy = raw_building.build_class(cls_name, builtins)
    return proxy

