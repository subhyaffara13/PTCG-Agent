
def test_null_movie_writer(anim):
    # Test running an animation with NullMovieWriter.
    plt.rcParams["savefig.facecolor"] = "auto"
    filename = "unused.null"
    dpi = 50
    savefig_kwargs = dict(foo=0)
    writer = NullMovieWriter()

    anim.save(filename, dpi=dpi, writer=writer,
              savefig_kwargs=savefig_kwargs)

    assert writer.fig == plt.figure(1)  # The figure used by anim fixture
    assert writer.outfile == filename
    assert writer.dpi == dpi
    assert writer.args == ()
    # we enrich the savefig kwargs to ensure we composite transparent
    # output to an opaque background
    for k, v in savefig_kwargs.items():
        assert writer.savefig_kwargs[k] == v
    assert writer._count == anim._save_count

