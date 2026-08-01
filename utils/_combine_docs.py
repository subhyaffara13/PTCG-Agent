
def _combine_docs(dist_family, *, include_examples=True):
    fields = set(NumpyDocString.sections)
    fields.remove('index')
    if not include_examples:
        fields.remove('Examples')

    doc = ClassDoc(dist_family)
    superdoc = ClassDoc(UnivariateDistribution)
    for field in fields:
        if field in {"Methods", "Attributes"}:
            doc[field] = superdoc[field]
        elif field in {"Summary"}:
            pass
        elif field == "Extended Summary":
            doc[field].append(_generate_domain_support(dist_family))
        elif field == 'Examples':
            doc[field] = [_generate_example(dist_family)]
        else:
            doc[field] += superdoc[field]
    return str(doc)

