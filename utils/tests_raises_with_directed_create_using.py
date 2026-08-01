
def tests_raises_with_directed_create_using(fn, create_using):
    with pytest.raises(nx.NetworkXError, match="Directed Graph not supported"):
        fn(create_using=create_using)
    # All these functions have `create_using` as the first positional argument too
    with pytest.raises(nx.NetworkXError, match="Directed Graph not supported"):
        fn(create_using)

