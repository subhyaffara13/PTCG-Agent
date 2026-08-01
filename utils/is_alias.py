
def is_alias(base, tensor):
    from torch.fx.experimental.symbolic_shapes import statically_known_true, sym_eq

    return all(
        statically_known_true(a)
        for a in [
            sym_eq(base.storage_offset(), tensor.storage_offset()),
            sym_eq(base.stride(), tensor.stride()),
            sym_eq(base.size(), tensor.size()),
        ]
    )

