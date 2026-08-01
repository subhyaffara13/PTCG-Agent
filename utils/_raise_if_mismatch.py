
def _raise_if_mismatch(expected, actual, prop_name, ranks, is_local=True):
    if is_local:
        if not isinstance(ranks, int):
            raise AssertionError
        if expected != actual:
            raise ValueError(
                f"Local shards' tensor {prop_name} property need to be the same on rank:{ranks}! "
                f"Found one local shard tensor {prop_name}={expected}, "
                f"the other local shard tensor {prop_name}={actual}."
            )
    else:
        # compare failure check across ranks, ranks list should have two rank
        if len(ranks) != 2:
            raise AssertionError
        if expected != actual:
            raise ValueError(
                f"ShardedTensor {prop_name} property does not match from different ranks! "
                f"Found {prop_name}={expected} on rank:{ranks[0]}, "
                f"and {prop_name}={actual} on rank:{ranks[1]}."
            )

