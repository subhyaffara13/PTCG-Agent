
def meshgrid_triangles(n):
    """
    Return (2*(N-1)**2, 3) array of triangles to mesh (N, N)-point np.meshgrid.
    """
    tri = []
    for i in range(n-1):
        for j in range(n-1):
            a = i + j*n
            b = (i+1) + j*n
            c = i + (j+1)*n
            d = (i+1) + (j+1)*n
            tri += [[a, b, d], [a, d, c]]
    return np.array(tri, dtype=np.int32)

