
def new_stream(*args: tuple[Any], **kwargs: Any) -> int:
    stream = torch.Stream(*args, **kwargs)  # type: ignore[no-matching-overload,call-overload]
    return register_graph_created_object(
        stream,
        StreamVariable.make_construct_in_graph_stream_fn(
            TupleVariable([]), ConstDictVariable({})
        ),
    )

