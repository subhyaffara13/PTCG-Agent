
def test_str_transform():
    # The str here should not be considered as "absolutely stable", and may be
    # reformatted later; this is just a smoketest for __str__.
    assert str(plt.subplot(projection="polar").transData) == """\
CompositeGenericTransform(
    CompositeGenericTransform(
        CompositeGenericTransform(
            TransformWrapper(
                BlendedAffine2D(
                    IdentityTransform(),
                    IdentityTransform())),
            CompositeAffine2D(
                Affine2D().scale(1.0),
                Affine2D().scale(1.0))),
        PolarTransform(
            PolarAxes(0.125,0.1;0.775x0.8),
            use_rmin=True)),
    CompositeGenericTransform(
        CompositeGenericTransform(
            PolarAffine(
                TransformWrapper(
                    BlendedAffine2D(
                        IdentityTransform(),
                        IdentityTransform())),
                LockableBbox(
                    Bbox(x0=0.0, y0=0.0, x1=6.283185307179586, y1=1.0),
                    [[-- --]
                     [-- --]])),
            BboxTransformFrom(
                _WedgeBbox(
                    (0.5, 0.5),
                    TransformedBbox(
                        Bbox(x0=0.0, y0=0.0, x1=6.283185307179586, y1=1.0),
                        CompositeAffine2D(
                            Affine2D().scale(1.0),
                            Affine2D().scale(1.0))),
                    LockableBbox(
                        Bbox(x0=0.0, y0=0.0, x1=6.283185307179586, y1=1.0),
                        [[-- --]
                         [-- --]])))),
        BboxTransformTo(
            TransformedBbox(
                Bbox(x0=0.125, y0=0.09999999999999998, x1=0.9, y1=0.9),
                BboxTransformTo(
                    TransformedBbox(
                        Bbox(x0=0.0, y0=0.0, x1=8.0, y1=6.0),
                        Affine2D().scale(80.0)))))))"""

