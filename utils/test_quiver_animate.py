
def test_quiver_animate():
    # Tests fix for #2616
    fig, ax = plt.subplots()
    Q = draw_quiver(ax, animated=True)
    ax.quiverkey(Q, 0.5, 0.88, 2, r'$2 \frac{m}{s}$',
                 labelpos='W', fontproperties={'weight': 'bold'})

