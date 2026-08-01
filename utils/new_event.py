
def new_event(*args: Any, **kwargs: Any) -> int:
    event = torch.Event(*args, **kwargs)
    return register_graph_created_object(
        event,
        EventVariable.make_construct_in_graph_event_fn(
            TupleVariable([]), ConstDictVariable({})
        ),
    )

