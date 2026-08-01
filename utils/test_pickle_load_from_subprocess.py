
def test_pickle_load_from_subprocess(fig_test, fig_ref, tmp_path):
    _generate_complete_test_figure(fig_ref)

    fp = tmp_path / 'sinus.pickle'
    assert not fp.exists()

    with fp.open('wb') as file:
        pickle.dump(fig_ref, file, pickle.HIGHEST_PROTOCOL)
    assert fp.exists()

    proc = subprocess_run_helper(
        _pickle_load_subprocess,
        timeout=60,
        extra_env={"PICKLE_FILE_PATH": str(fp), "MPLBACKEND": "Agg"},
    )

    loaded_fig = pickle.loads(ast.literal_eval(proc.stdout))

    loaded_fig.canvas.draw()

    fig_test.set_size_inches(loaded_fig.get_size_inches())
    fig_test.figimage(loaded_fig.canvas.renderer.buffer_rgba())

    plt.close(loaded_fig)

