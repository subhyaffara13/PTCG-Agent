
def register_rng_prim(name, schema, impl_aten, impl_meta, doc, tags=None):
    rngprim_def = torch.library.custom_op(
        "rngprims::" + name, impl_aten, mutates_args=(), schema=schema
    )

    rngprim_def.register_fake(impl_meta)

    prim_packet = getattr(torch._ops.ops.rngprims, name)
    prim = prim_packet.default
    if tags:
        prim._tags = tags

    for p in (prim_packet, prim):
        p.__doc__ = doc
        p.return_type = torch._prims_common.RETURN_TYPE.NEW  # type: ignore[attr-defined]

        p.schema = name + schema
        p.impl_aten = impl_aten
        p.prim_meta_impl = impl_meta

