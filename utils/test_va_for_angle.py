
def test_va_for_angle():
    text_instance = Text()
    angles = np.arange(0, 360.1, 0.1)
    for angle in angles:
        alignment = text_instance._va_for_angle(angle)
        assert alignment in ['center', 'top', 'baseline']

