
def replica_only_strategy(op_schema: OpSchema) -> StrategyType:
    """Only allow replication on the input/output."""
    input_strategy = op_schema.args_schema[0]
    if not isinstance(input_strategy, OpStrategy):
        raise AssertionError(f"Expected OpStrategy, got {type(input_strategy)}")
    mesh = input_strategy.mesh
    replicate_spec = DTensorSpec(mesh, tuple([Replicate()] * mesh.ndim))
    return OpStrategy([OpSpec(replicate_spec)])

