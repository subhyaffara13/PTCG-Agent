
def baddbmm_strategy(op_schema: OpSchema) -> OpStrategy:
    mesh = op_schema.get_mesh_from_args()
    return _addmm_like_strategy("bmk,bkn->bmn", mesh, op_schema)

