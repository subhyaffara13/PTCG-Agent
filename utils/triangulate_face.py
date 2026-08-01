
def triangulate_face(embedding, v1, v2):
    """Triangulates the face given by half edge (v, w)

    Parameters
    ----------
    embedding : nx.PlanarEmbedding
    v1 : node
        The half-edge (v1, v2) belongs to the face that gets triangulated
    v2 : node
    """
    _, v3 = embedding.next_face_half_edge(v1, v2)
    _, v4 = embedding.next_face_half_edge(v2, v3)
    if v1 in (v2, v3):
        # The component has less than 3 nodes
        return
    while v1 != v4:
        # Add edge if not already present on other side
        if embedding.has_edge(v1, v3):
            # Cannot triangulate at this position
            v1, v2, v3 = v2, v3, v4
        else:
            # Add edge for triangulation
            embedding.add_half_edge(v1, v3, ccw=v2)
            embedding.add_half_edge(v3, v1, cw=v2)
            v1, v2, v3 = v1, v3, v4
        # Get next node
        _, v4 = embedding.next_face_half_edge(v2, v3)

