
def test_add_subplot_subclass():
    fig = plt.figure()
    fig.add_subplot(axes_class=Axes)
    with pytest.raises(ValueError):
        fig.add_subplot(axes_class=Axes, projection="3d")
    with pytest.raises(ValueError):
        fig.add_subplot(axes_class=Axes, polar=True)
    with pytest.raises(ValueError):
        fig.add_subplot(projection="3d", polar=True)
    with pytest.raises(TypeError):
        fig.add_subplot(projection=42)

