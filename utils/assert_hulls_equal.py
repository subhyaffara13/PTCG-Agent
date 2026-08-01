
def assert_hulls_equal(points, facets_1, facets_2):
    # Check that two convex hulls constructed from the same point set
    # are equal

    facets_1 = set(map(sorted_tuple, facets_1))
    facets_2 = set(map(sorted_tuple, facets_2))

    if facets_1 != facets_2 and points.shape[1] == 2:
        # The direct check fails for the pathological cases
        # --- then the convex hull from Delaunay differs (due
        # to rounding error etc.) from the hull computed
        # otherwise, by the question whether (tricoplanar)
        # points that lie almost exactly on the hull are
        # included as vertices of the hull or not.
        #
        # So we check the result, and accept it if the Delaunay
        # hull line segments are a subset of the usual hull.

        eps = 1000 * np.finfo(float).eps

        for a, b in facets_1:
            for ap, bp in facets_2:
                t = points[bp] - points[ap]
                t /= np.linalg.norm(t)       # tangent
                n = np.array([-t[1], t[0]])  # normal

                # check that the two line segments are parallel
                # to the same line
                c1 = np.dot(n, points[b] - points[ap])
                c2 = np.dot(n, points[a] - points[ap])
                if not np.allclose(np.dot(c1, n), 0):
                    continue
                if not np.allclose(np.dot(c2, n), 0):
                    continue

                # Check that the segment (a, b) is contained in (ap, bp)
                c1 = np.dot(t, points[a] - points[ap])
                c2 = np.dot(t, points[b] - points[ap])
                c3 = np.dot(t, points[bp] - points[ap])
                if c1 < -eps or c1 > c3 + eps:
                    continue
                if c2 < -eps or c2 > c3 + eps:
                    continue

                # OK:
                break
            else:
                raise AssertionError("comparison fails")

        # it was OK
        return

    assert_equal(facets_1, facets_2)

