
def _generate_dodecahedron():

    x1 = _generate_cube()
    x2 = np.array([[0, -phi, -1 / phi],
                   [0, -phi, +1 / phi],
                   [0, +phi, -1 / phi],
                   [0, +phi, +1 / phi]])
    x3 = np.array([[-1 / phi, 0, -phi],
                   [+1 / phi, 0, -phi],
                   [-1 / phi, 0, +phi],
                   [+1 / phi, 0, +phi]])
    x4 = np.array([[-phi, -1 / phi, 0],
                   [-phi, +1 / phi, 0],
                   [+phi, -1 / phi, 0],
                   [+phi, +1 / phi, 0]])
    return np.concatenate((x1, x2, x3, x4))

