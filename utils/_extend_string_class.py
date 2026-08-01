
def _extend_string_class(class_node, code, rvalue):
    """Function to extend builtin str/unicode class."""
    code = code.format(rvalue=rvalue)
    fake = AstroidBuilder(AstroidManager()).string_build(code)["whatever"]
    for method in fake.mymethods():
        method.parent = class_node
        method.lineno = None
        method.col_offset = None
        if "__class__" in method.locals:
            method.locals["__class__"] = [class_node]
        class_node.locals[method.name] = [method]
        method.parent = class_node

