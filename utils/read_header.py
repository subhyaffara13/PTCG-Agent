
def read_header(ofile):
    """Read the header of the iterable ofile."""
    i = next(ofile)

    # Pass first comments
    while r_comment.match(i):
        i = next(ofile)

    # Header is everything up to DATA attribute ?
    relation = None
    attributes = []
    while not r_datameta.match(i):
        m = r_headerline.match(i)
        if m:
            isattr = r_attribute.match(i)
            if isattr:
                attr, i = tokenize_attribute(ofile, i)
                attributes.append(attr)
            else:
                isrel = r_relation.match(i)
                if isrel:
                    relation = isrel.group(1)
                else:
                    raise ValueError(f"Error parsing line {i}")
                i = next(ofile)
        else:
            i = next(ofile)

    return relation, attributes

