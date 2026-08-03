from pathlib import Path


def test_image_comparison_expect_rms(im1, im2, tol, expect_rms, tmp_path,
                                     monkeypatch):
    """
    Compare two images, expecting a particular RMS error.

    im1 and im2 are filenames relative to the baseline_dir directory.

    tol is the tolerance to pass to compare_images.

    expect_rms is the expected RMS value, or None. If None, the test will
    succeed if compare_images succeeds. Otherwise, the test will succeed if
    compare_images fails and returns an RMS error almost equal to this value.
    """
    # Change the working directory using monkeypatch to use a temporary
    # test specific directory
    monkeypatch.chdir(tmp_path)
    baseline_dir, result_dir = map(Path, _image_directories(lambda: "dummy"))
    # Copy "test" image to result_dir, so that compare_images writes
    # the diff to result_dir, rather than to the source tree
    result_im2 = result_dir / im1
    shutil.copyfile(baseline_dir / im2, result_im2)
    results = compare_images(
        baseline_dir / im1, result_im2, tol=tol, in_decorator=True)

    if expect_rms is None:
        assert results is None
    else:
        assert results is not None
        assert results['rms'] == approx(expect_rms, abs=1e-4)

