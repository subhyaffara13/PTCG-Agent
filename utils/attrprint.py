
def attrprint(d, delimiter=', '):
    """ Print a dictionary of attributes

    Examples
    ========

    >>> from sympy.printing.dot import attrprint
    >>> print(attrprint({'color': 'blue', 'shape': 'ellipse'}))
    "color"="blue", "shape"="ellipse"
    """
    return delimiter.join('"%s"="%s"'%item for item in sorted(d.items()))

