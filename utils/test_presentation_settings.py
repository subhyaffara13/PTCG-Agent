
def test_presentation_settings():
    raises(TypeError, lambda: mathml(x, printer='presentation',
                                     method="garbage"))

