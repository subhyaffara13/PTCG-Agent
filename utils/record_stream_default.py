
def record_stream_default(func, *args, **kwargs) -> None:
    inp = args[0]
    stream = args[1]
    # ensure all components live until stream computation completes
    func(inp._values, stream)
    func(inp._offsets, stream)
    if inp._lengths is not None:
        func(inp._lengths, stream)

