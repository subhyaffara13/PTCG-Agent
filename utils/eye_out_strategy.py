
def eye_out_strategy(op_schema: OpSchema) -> OpStrategy:
    """
    Strategy for torch.eye with out= parameter.
    The sharding is determined by the out tensor's placement.
    """
    # eye.m_out has signature: eye(int n, int m, *, Tensor(a!) out) -> Tensor(a!)
    # The out kwarg is a DTensor that determines the sharding
    out_spec = op_schema.kwargs_schema["out"]
    if not isinstance(out_spec, OpStrategy):
        raise AssertionError(f"Expected OpStrategy for out, got {type(out_spec)}")

    return OpStrategy(
        [
            OpSpec(
                output_specs=strategy.output_spec,
                input_specs=[strategy.output_spec],  # out is both input and output
                redistribute_cost=[[0.0]],
            )
            for strategy in out_spec.strategies
        ]
    )

