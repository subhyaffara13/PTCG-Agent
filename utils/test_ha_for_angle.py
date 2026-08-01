
def test_ha_for_angle():
    text_instance = Text()
    angles = np.arange(0, 360.1, 0.1)
    for angle in angles:
        alignment = text_instance._ha_for_angle(angle)
        assert alignment in ['center', 'left', 'right']

