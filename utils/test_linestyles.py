
def test_linestyles(style):
    delta = 0.025
    x = np.arange(-3.0, 3.0, delta)
    y = np.arange(-2.0, 2.0, delta)
    X, Y = np.meshgrid(x, y)
    Z1 = np.exp(-X**2 - Y**2)
    Z2 = np.exp(-(X - 1)**2 - (Y - 1)**2)
    Z = (Z1 - Z2) * 2

    # Positive contour defaults to solid
    fig1, ax1 = plt.subplots()
    CS1 = ax1.contour(X, Y, Z, 6, colors='k')
    ax1.clabel(CS1, fontsize=9, inline=True)
    ax1.set_title('Single color - positive contours solid (default)')
    assert CS1.linestyles is None  # default

    # Change linestyles using linestyles kwarg
    fig2, ax2 = plt.subplots()
    CS2 = ax2.contour(X, Y, Z, 6, colors='k', linestyles=style)
    ax2.clabel(CS2, fontsize=9, inline=True)
    ax2.set_title(f'Single color - positive contours {style}')
    assert CS2.linestyles == style

    # Ensure linestyles do not change when negative_linestyles is defined
    fig3, ax3 = plt.subplots()
    CS3 = ax3.contour(X, Y, Z, 6, colors='k', linestyles=style,
                      negative_linestyles='dashdot')
    ax3.clabel(CS3, fontsize=9, inline=True)
    ax3.set_title(f'Single color - positive contours {style}')
    assert CS3.linestyles == style

