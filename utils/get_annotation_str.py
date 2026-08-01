
def get_annotation_str(annotation):
    """
    Convert an AST node containing a type annotation to the string present in the source
    that represents the same annotation.
    """
    if isinstance(annotation, ast.Name):
        return annotation.id
    elif isinstance(annotation, ast.Attribute):
        return ".".join([get_annotation_str(annotation.value), annotation.attr])
    elif isinstance(annotation, ast.Subscript):
        # In Python3.9+ subscript indices are not wrapped in ast.Index
        subscript_slice = annotation.slice
        return f"{get_annotation_str(annotation.value)}[{get_annotation_str(subscript_slice)}]"
    elif isinstance(annotation, ast.Tuple):
        return ",".join([get_annotation_str(elt) for elt in annotation.elts])
    elif isinstance(annotation, ast.Constant):
        return f"{annotation.value}"

    # If an AST node is not handled here, it's probably handled in ScriptTypeParser.
    return None

