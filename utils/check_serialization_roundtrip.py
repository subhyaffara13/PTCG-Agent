
def check_serialization_roundtrip(irs: dict[str, ModuleIR]) -> None:
    """Check that we can serialize modules out and deserialize them to the same thing."""
    serialized = {k: ir.serialize() for k, ir in irs.items()}

    ctx = DeserMaps({}, {})
    irs2 = deserialize_modules(serialized, ctx)
    assert irs.keys() == irs2.keys()

    for k in irs:
        assert_modules_same(irs[k], irs2[k])

