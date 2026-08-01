
def test_barbs_flip():
    """Test barbs with an array for flip_barb."""
    x = np.linspace(-5, 5, 5)
    X, Y = np.meshgrid(x, x)
    U, V = 12*X, 12*Y
    fig, ax = plt.subplots()
    ax.barbs(X, Y, U, V, fill_empty=True, rounding=False, pivot=1.7,
             sizes=dict(emptybarb=0.25, spacing=0.2, height=0.3),
             flip_barb=Y < 0)

