
def test_mappable_no_alpha():
    fig, ax = plt.subplots()
    sm = cm.ScalarMappable(norm=mcolors.Normalize(), cmap='viridis')
    fig.colorbar(sm, ax=ax)
    sm.set_cmap('plasma')
    plt.draw()

