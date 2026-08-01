
def test_create_using(generator, kwargs, create_using_instance):
    class DummyGraph(nx.Graph):
        pass

    class DummyDiGraph(nx.DiGraph):
        pass

    create_using_type = DummyDiGraph if kwargs.get("directed") else DummyGraph
    create_using = create_using_type() if create_using_instance else create_using_type
    graph = generator(**kwargs, create_using=create_using)
    assert isinstance(graph, create_using_type)

