
def test_marker_transformed(marker, transform, expected):
    new_marker = marker.transformed(transform)
    assert new_marker is not marker
    assert new_marker.get_user_transform() == expected
    assert marker._user_transform is not new_marker._user_transform

