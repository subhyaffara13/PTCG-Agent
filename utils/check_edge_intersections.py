
def check_edge_intersections(G, pos):
    """Check all edges in G for intersections.

    Raises an exception if an intersection is found.

    Parameters
    ----------
    G : NetworkX graph
    pos : dict
        Maps every node to a tuple (x, y) representing its position

    """
    for a, b in G.edges():
        for c, d in G.edges():
            # Check if end points are different
            if a != c and b != d and b != c and a != d:
                x1, y1 = pos[a]
                x2, y2 = pos[b]
                x3, y3 = pos[c]
                x4, y4 = pos[d]
                determinant = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
                if determinant != 0:  # the lines are not parallel
                    # calculate intersection point, see:
                    # https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection
                    px = (x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (
                        x3 * y4 - y3 * x4
                    ) / determinant
                    py = (x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (
                        x3 * y4 - y3 * x4
                    ) / determinant

                    # Check if intersection lies between the points
                    if point_in_between(pos[a], pos[b], (px, py)) and point_in_between(
                        pos[c], pos[d], (px, py)
                    ):
                        msg = f"There is an intersection at {px},{py}"
                        raise nx.NetworkXException(msg)

                #  Check overlap
                msg = "A node lies on a edge connecting two other nodes"
                if (
                    point_in_between(pos[a], pos[b], pos[c])
                    or point_in_between(pos[a], pos[b], pos[d])
                    or point_in_between(pos[c], pos[d], pos[a])
                    or point_in_between(pos[c], pos[d], pos[b])
                ):
                    raise nx.NetworkXException(msg)

