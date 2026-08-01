
def test_gh_24751():
    points = np.array([[0.0, 0.0, 0.0]])
    points.flags.writeable = False
    rot = Rotation.from_euler("z", 0.0)
    rot.apply(points)

