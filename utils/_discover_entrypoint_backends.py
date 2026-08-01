
def _discover_entrypoint_backends() -> None:
    # importing here so it will pick up the mocked version in test_backends.py
    from importlib.metadata import entry_points

    group_name = "torch_dynamo_backends"
    eps = entry_points(group=group_name)
    # pyrefly: ignore [bad-index]
    eps_dict = {name: eps[name] for name in eps.names}
    for backend_name in eps_dict:
        _BACKENDS[backend_name] = eps_dict[backend_name]

