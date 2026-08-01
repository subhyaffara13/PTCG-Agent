
def try_get_buf_size(buf_name: str) -> int | None:
    buf = V.graph.try_get_buffer(buf_name)
    if not buf:
        return None
    return V.graph.sizevars.optimization_hint(sympy_product(buf.get_size()))

