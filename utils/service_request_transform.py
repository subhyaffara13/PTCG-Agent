
def service_request_transform(node: ClassDef) -> ClassDef:
    """Transform ServiceResource to look like dynamic classes."""
    code = """
    def __getattr__(self, attr):
        return 0
    """
    func_getattr = extract_node(code)
    node.locals["__getattr__"] = [func_getattr]
    return node

