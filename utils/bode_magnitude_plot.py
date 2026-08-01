
def bode_magnitude_plot(system, initial_exp=-5, final_exp=5,
    color='b', show_axes=False, grid=True, show=True, freq_unit='rad/sec', **kwargs):
    r"""
    Returns the Bode magnitude plot of a continuous-time system.

    See ``bode_plot`` for all the parameters.
    """
    x, y = bode_magnitude_numerical_data(system, initial_exp=initial_exp,
        final_exp=final_exp, freq_unit=freq_unit)
    plt.plot(x, y, color=color, **kwargs)
    plt.xscale('log')


    plt.xlabel('Frequency (%s) [Log Scale]' % freq_unit)
    plt.ylabel('Magnitude (dB)')
    plt.title(f'Bode Plot (Magnitude) of ${latex(system)}$', pad=20)

    if grid:
        plt.grid(True)
    if show_axes:
        plt.axhline(0, color='black')
        plt.axvline(0, color='black')
    if show:
        plt.show()
        return

    return plt

