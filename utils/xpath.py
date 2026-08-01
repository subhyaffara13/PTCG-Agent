
def xpath(path):
    # compile XPath upfront, caching result to reuse on multiple elements
    return etree.XPath(path, namespaces=NAMESPACES)

