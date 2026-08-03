import itertools
import time

def test_warn_big_data_best_loc(monkeypatch):
    # Force _find_best_position to think it took a long time.
    counter = itertools.count(0, step=1.5)
    monkeypatch.setattr(time, 'perf_counter', lambda: next(counter))

    fig, ax = plt.subplots()
    fig.canvas.draw()  # So that we can call draw_artist later.

    # Place line across all possible legend locations.
    x = [0.9, 0.1, 0.1, 0.9, 0.9, 0.5]
    y = [0.95, 0.95, 0.05, 0.05, 0.5, 0.5]
    ax.plot(x, y, 'o-', label='line')

    with rc_context({'legend.loc': 'best'}):
        legend = ax.legend()
    with pytest.warns(UserWarning,
                      match='Creating legend with loc="best" can be slow with large '
                      'amounts of data.') as records:
        fig.draw_artist(legend)  # Don't bother drawing the lines -- it's slow.
    # The _find_best_position method of Legend is called twice, duplicating
    # the warning message.
    assert len(records) == 2

