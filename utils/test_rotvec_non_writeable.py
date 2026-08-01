
def test_rotvec_non_writeable():
    rotvec = np.array([0, 0, 1]) * np.pi / 2
    rotvec.flags.writeable = False
    Rotation.from_rotvec(rotvec)

