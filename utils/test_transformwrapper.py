
def test_transformwrapper():
    t = mtransforms.TransformWrapper(mtransforms.Affine2D())
    with pytest.raises(ValueError, match=(
            r"The input and output dims of the new child \(1, 1\) "
            r"do not match those of current child \(2, 2\)")):
        t.set(scale.LogTransform(10))

