
def create_op_support(is_node_supported: IsNodeSupported) -> OperatorSupportBase:
    """Wraps a `IsNodeSupported` function into an `OperatorSupportBase` instance

    `IsNodeSupported` has the same call signature as
    `OperatorSupportBase.is_node_supported`
    """

    class FunctionalOperatorSupport(OperatorSupportBase):
        def is_node_supported(
            self, submodules: t.Mapping[str, torch.nn.Module], node: torch.fx.Node
        ) -> bool:
            return is_node_supported(submodules, node)

    return FunctionalOperatorSupport()

