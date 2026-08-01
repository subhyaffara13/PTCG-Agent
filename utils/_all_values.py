
def _all_values(model: ir.Model):
    """Yield all values in a model."""
    # Yield all values in the model
    yield from model.graph.inputs
    yield from model.graph.initializers.values()
    for node in ir.traversal.RecursiveGraphIterator(model.graph):
        yield from node.outputs
    # Yield all values in functions
    for function in model.functions.values():
        yield from function.inputs
        for node in ir.traversal.RecursiveGraphIterator(function):
            yield from node.outputs

