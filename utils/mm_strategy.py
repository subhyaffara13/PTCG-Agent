
def mm_strategy(op_schema: OpSchema) -> OpStrategy:
    mesh = op_schema.get_mesh_from_args()
    return _mm_like_strategy("mk,kn->mn", mesh, op_schema)

