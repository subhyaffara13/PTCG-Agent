
def test_evaluate_error_inputs():
    gen = FastGeneratorInversion(stats.norm())
    with pytest.raises(ValueError, match="size must be an integer"):
        gen.evaluate_error(size=3.5)
    with pytest.raises(ValueError, match="size must be an integer"):
        gen.evaluate_error(size=(3, 3))

