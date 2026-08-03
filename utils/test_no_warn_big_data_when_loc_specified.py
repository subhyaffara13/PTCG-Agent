import itertools
import time

def test_no_warn_big_data_when_loc_specified(monkeypatch):
    # Force _find_best_position to think it took a long time.
    counter = itertools.count(0, step=1.5)
    monkeypatch.setattr(time, 'perf_counter', lambda: next(counter))

    fig, ax = plt.subplots()
    fig.canvas.draw()

    # Place line across all possible legend locations.
    x = [0.9, 0.1, 0.1, 0.9, 0.9, 0.5]
    y = [0.95, 0.95, 0.05, 0.05, 0.5, 0.5]
    ax.plot(x, y, 'o-', label='line')

    legend = ax.legend('best')
    fig.draw_artist(legend)  # Check that no warning is emitted.

