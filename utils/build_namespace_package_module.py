
def build_namespace_package_module(name: str, path: Sequence[str]) -> nodes.Module:
    module = nodes.Module(name, path=path, package=True)
    module.postinit(body=[], doc_node=None)
    return module

