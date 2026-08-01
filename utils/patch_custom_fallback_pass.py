
def patch_custom_fallback_pass(predicate: Callable[[torch.fx.Node], bool]) -> contextlib.ContextDecorator:
    """
    Create a custom pass which falls back based on the provided predicate. For example,
    we could provide a predicate which returns True for all aten.add.default nodes.
    Returns a context activating the pass.
    """
    class Pass(CustomGraphPass):
        def __call__(self, graph: torch.fx.Graph):
            for node in graph.nodes:
                if predicate(node):
                    node.meta["should_fallback"] = True

        def uuid(self):
            return None


    return config.patch(post_grad_custom_pre_pass=Pass())

