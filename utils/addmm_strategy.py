
def addmm_strategy(op_schema: OpSchema) -> OpStrategy:
    mesh = op_schema.get_mesh_from_args()
    return _addmm_like_strategy("mk,kn->mn", mesh, op_schema)

