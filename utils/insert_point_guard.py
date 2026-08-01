
def insert_point_guard(
    self: torch._C.Graph, insert_point: torch._C.Node | torch._C.Block
) -> _InsertPoint:
    return _InsertPoint(self, insert_point)

