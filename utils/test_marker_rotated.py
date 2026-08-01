
def test_marker_rotated(marker, deg, rad, expected):
    new_marker = marker.rotated(deg=deg, rad=rad)
    assert new_marker is not marker
    assert new_marker.get_user_transform() == expected
    assert marker._user_transform is not new_marker._user_transform

