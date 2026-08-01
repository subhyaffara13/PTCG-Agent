
def tetrahedral(cls):
    g1 = np.eye(4)
    c = 0.5
    g2 = np.array([[c, -c, -c, +c],
                   [c, -c, +c, +c],
                   [c, +c, -c, +c],
                   [c, +c, +c, +c],
                   [c, -c, -c, -c],
                   [c, -c, +c, -c],
                   [c, +c, -c, -c],
                   [c, +c, +c, -c]])
    return cls.from_quat(np.concatenate((g1, g2)))

