
def pytree_register_structseq(cls):
    def structseq_flatten(structseq):
        return list(structseq), None

    def structseq_flatten_with_keys(structseq):
        values, context = structseq_flatten(structseq)
        return [(SequenceKey(i), v) for i, v in enumerate(values)], context

    def structseq_unflatten(values, context):
        return cls(values)

    register_pytree_node(
        cls,
        structseq_flatten,
        structseq_unflatten,
        flatten_with_keys_fn=structseq_flatten_with_keys,
    )

