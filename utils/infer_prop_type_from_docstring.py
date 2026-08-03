import re

def infer_prop_type_from_docstring(docstr: str | None) -> str | None:
    """Check for Google/Numpy style docstring type annotation for a property.

    The docstring has the format "<type>: <descriptions>".
    In the type string, we allow the following characters:
    * dot: because sometimes classes are annotated using full path
    * brackets: to allow type hints like List[int]
    * comma/space: things like Tuple[int, int]
    """
    if not docstr:
        return None
    test_str = r"^([a-zA-Z0-9_, \.\[\]]*): "
    m = re.match(test_str, docstr)
    return m.group(1) if m else None

