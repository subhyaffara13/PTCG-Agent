
def test_negative_linestyles(style):
    delta = 0.025
    x = np.arange(-3.0, 3.0, delta)
    y = np.arange(-2.0, 2.0, delta)
    X, Y = np.meshgrid(x, y)
    Z1 = np.exp(-X**2 - Y**2)
    Z2 = np.exp(-(X - 1)**2 - (Y - 1)**2)
    Z = (Z1 - Z2) * 2

    # Negative contour defaults to dashed
    fig1, ax1 = plt.subplots()
    CS1 = ax1.contour(X, Y, Z, 6, colors='k')
    ax1.clabel(CS1, fontsize=9, inline=True)
    ax1.set_title('Single color - negative contours dashed (default)')
    assert CS1.negative_linestyles == 'dashed'  # default

    # Change negative_linestyles using rcParams
    plt.rcParams['contour.negative_linestyle'] = style
    fig2, ax2 = plt.subplots()
    CS2 = ax2.contour(X, Y, Z, 6, colors='k')
    ax2.clabel(CS2, fontsize=9, inline=True)
    ax2.set_title(f'Single color - negative contours {style}'
                   '(using rcParams)')
    assert CS2.negative_linestyles == style

    # Change negative_linestyles using negative_linestyles kwarg
    fig3, ax3 = plt.subplots()
    CS3 = ax3.contour(X, Y, Z, 6, colors='k', negative_linestyles=style)
    ax3.clabel(CS3, fontsize=9, inline=True)
    ax3.set_title(f'Single color - negative contours {style}')
    assert CS3.negative_linestyles == style

    # Ensure negative_linestyles do not change when linestyles is defined
    fig4, ax4 = plt.subplots()
    CS4 = ax4.contour(X, Y, Z, 6, colors='k', linestyles='dashdot',
                      negative_linestyles=style)
    ax4.clabel(CS4, fontsize=9, inline=True)
    ax4.set_title(f'Single color - negative contours {style}')
    assert CS4.negative_linestyles == style

