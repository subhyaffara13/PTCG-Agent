
def nonaffine_identity():
    """Non-affine identity transform for compositing with any affine transform"""
    class NonAffineIdentityTransform(Transform):
        input_dims = 2
        output_dims = 2

        def inverted(self):
            return self
    return NonAffineIdentityTransform()

