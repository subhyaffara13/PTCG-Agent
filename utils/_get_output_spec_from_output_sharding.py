
def _get_output_spec_from_output_sharding(
    output_sharding: OutputSharding,
) -> DTensorSpec:
    """
    Util function to extract output spec from output sharding.
    """
    if isinstance(output_sharding.output_spec, DTensorSpec):
        return output_sharding.output_spec
    else:
        # For ops that return multiple outputs, the outputs should have the same output spec
        if not isinstance(output_sharding.output_spec, Sequence):
            raise AssertionError
        if output_sharding.output_spec[0] is None:
            raise AssertionError
        output_sharding.output_spec[0].tensor_meta = None
        return output_sharding.output_spec[0]

