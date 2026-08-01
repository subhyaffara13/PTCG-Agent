
def test_savefig_backend():
    fig = plt.figure()
    # Intentionally use an invalid module name.
    with pytest.raises(ModuleNotFoundError, match="No module named '@absent'"):
        fig.savefig("test", backend="module://@absent")
    with pytest.raises(ValueError,
                       match="The 'pdf' backend does not support png output"):
        fig.savefig("test.png", backend="pdf")

