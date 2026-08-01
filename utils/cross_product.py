
def cross_product(v1, v2, v3):
    """Returns the cross-product of vectors (v2 - v1) and (v3 - v1)
    That is : (v2 - v1) X (v3 - v1)
    """
    v2 = [v2[j] - v1[j] for j in range(0, 3)]
    v3 = [v3[j] - v1[j] for j in range(0, 3)]
    return [v3[2] * v2[1] - v3[1] * v2[2],
            v3[0] * v2[2] - v3[2] * v2[0],
            v3[1] * v2[0] - v3[0] * v2[1]]

