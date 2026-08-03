from typing import Any

def generate_non_native_lazy_ir_nodes(
    non_native: list[dict[str, Any]], gen_lazy_ir: GenLazyIR
) -> list[str]:
    """Generate the non-native lazy IR node classes"""
    nodes = []
    for op in non_native:
        # Set default properties for Non-Native IRs
        properties = LazyIrProperties("ShapeCache", "CanBeReused", "LowerDeclOnly")
        for p in op.get("properties", []):
            setattr(properties, p, True)

        # non-native is assumed to want symint bindings if you wrote symint
        schema = LazyIrSchema(FunctionSchema.parse(op["func"]), properties, symint=True)
        schema.opkind = op.get("opkind")
        nodes.append(gen_lazy_ir.gen(schema)[0])

    return nodes

