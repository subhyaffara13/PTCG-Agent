from pathlib import Path


def test_clipping_of_log():
    # issue 804
    path = Path._create_closed([(0.2, -99), (0.4, -99), (0.4, 20), (0.2, 20)])
    # something like this happens in plotting logarithmic histograms
    trans = mtransforms.BlendedGenericTransform(
        mtransforms.Affine2D(), scale.LogTransform(10, 'clip'))
    tpath = trans.transform_path_non_affine(path)
    result = tpath.iter_segments(trans.get_affine(),
                                 clip=(0, 0, 100, 100),
                                 simplify=False)
    tpoints, tcodes = zip(*result)
    assert_allclose(tcodes, path.codes[:-1])  # No longer closed.

