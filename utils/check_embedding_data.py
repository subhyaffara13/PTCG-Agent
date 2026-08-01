
def check_embedding_data(embedding_data):
    """Checks that the planar embedding of the input is correct"""
    embedding = nx.PlanarEmbedding()
    embedding.set_data(embedding_data)
    pos_fully = nx.combinatorial_embedding_to_pos(embedding, False)
    msg = "Planar drawing does not conform to the embedding (fully triangulation)"
    assert planar_drawing_conforms_to_embedding(embedding, pos_fully), msg
    check_edge_intersections(embedding, pos_fully)
    pos_internally = nx.combinatorial_embedding_to_pos(embedding, True)
    msg = "Planar drawing does not conform to the embedding (internal triangulation)"
    assert planar_drawing_conforms_to_embedding(embedding, pos_internally), msg
    check_edge_intersections(embedding, pos_internally)

