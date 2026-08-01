
def _visit_query_reference_node(self, node):
    """
    Resolve *node* into query strings on its ``reference`` children.

    Then act as if this is a `~docutils.nodes.literal`.
    """
    query = node.to_query_string()
    for refnode in node.findall(nodes.reference):
        uri = urlsplit(refnode['refuri'])._replace(query=query)
        refnode['refuri'] = urlunsplit(uri)

    self.visit_literal(node)

