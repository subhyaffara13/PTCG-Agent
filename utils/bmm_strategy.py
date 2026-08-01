
def bmm_strategy(op_schema: OpSchema) -> OpStrategy:
    mesh = op_schema.get_mesh_from_args()
    return _mm_like_strategy("bmk,bkn->bmn", mesh, op_schema)

