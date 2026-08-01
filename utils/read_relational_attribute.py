
def read_relational_attribute(ofile, relational_attribute, i):
    """Read the nested attributes of a relational attribute"""

    r_end_relational = re.compile(r'^@[Ee][Nn][Dd]\s*' +
                                  relational_attribute.name + r'\s*$')

    while not r_end_relational.match(i):
        m = r_headerline.match(i)
        if m:
            isattr = r_attribute.match(i)
            if isattr:
                attr, i = tokenize_attribute(ofile, i)
                relational_attribute.attributes.append(attr)
            else:
                raise ValueError(f"Error parsing line {i}")
        else:
            i = next(ofile)

    i = next(ofile)
    return i

