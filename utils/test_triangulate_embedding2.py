
def test_triangulate_embedding2():
    embedding = nx.PlanarEmbedding()
    embedding.connect_components(1, 2)
    expected_embedding = {1: [2], 2: [1]}
    check_triangulation(embedding, expected_embedding)

