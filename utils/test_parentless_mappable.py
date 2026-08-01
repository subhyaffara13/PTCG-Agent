
def test_parentless_mappable():
    pc = mpl.collections.PatchCollection([], cmap=plt.get_cmap('viridis'), array=[])
    with pytest.raises(ValueError, match='Unable to determine Axes to steal'):
        plt.colorbar(pc)

