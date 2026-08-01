
def _raise_on_directed(func):
    """
    A decorator which inspects the `create_using` argument and raises a
    NetworkX exception when `create_using` is a DiGraph (class or instance) for
    graph generators that do not support directed outputs.

    `create_using` may be a keyword argument or the first positional argument.
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        create_using = args[0] if args else kwargs.get("create_using")
        if create_using is not None:
            G = nx.empty_graph(create_using=create_using)
            if G.is_directed():
                raise NetworkXError("Directed Graph not supported in create_using")
        return func(*args, **kwargs)

    return wrapper

