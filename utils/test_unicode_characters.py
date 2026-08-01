
def test_unicode_characters():
    # Smoke test to see that Unicode characters does not cause issues
    # See #23019
    plt.rcParams['text.usetex'] = True
    fig, ax = plt.subplots()
    ax.set_ylabel('\\textit{Velocity (\N{DEGREE SIGN}/sec)}')
    ax.set_xlabel('\N{VULGAR FRACTION ONE QUARTER}Öøæ')
    fig.canvas.draw()

    # But not all characters.
    # Should raise RuntimeError, not UnicodeDecodeError
    with pytest.raises(RuntimeError):
        ax.set_title('\N{SNOWMAN}')
        fig.canvas.draw()

