
def test_arrow_simple():
    # Simple image test for ax.arrow
    # kwargs that take discrete values
    length_includes_head = (True, False)
    shape = ('full', 'left', 'right')
    head_starts_at_zero = (True, False)
    # Create outer product of values
    kwargs = product(length_includes_head, shape, head_starts_at_zero)

    fig, axs = plt.subplots(3, 4)
    for i, (ax, kwarg) in enumerate(zip(axs.flat, kwargs)):
        ax.set_xlim(-2, 2)
        ax.set_ylim(-2, 2)
        # Unpack kwargs
        (length_includes_head, shape, head_starts_at_zero) = kwarg
        theta = 2 * np.pi * i / 12
        # Draw arrow
        ax.arrow(0, 0, np.sin(theta), np.cos(theta),
                 width=theta/100,
                 length_includes_head=length_includes_head,
                 shape=shape,
                 head_starts_at_zero=head_starts_at_zero,
                 head_width=theta / 10,
                 head_length=theta / 10)

