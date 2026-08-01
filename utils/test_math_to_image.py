
def test_math_to_image(tmp_path):
    mathtext.math_to_image('$x^2$', tmp_path / 'example.png')
    mathtext.math_to_image('$x^2$', io.BytesIO())
    mathtext.math_to_image('$x^2$', io.BytesIO(), color='Maroon')

