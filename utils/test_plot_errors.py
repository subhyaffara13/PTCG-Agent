
def test_plot_errors():
    with pytest.raises(TypeError, match=r"plot\(\) got an unexpected keyword"):
        plt.plot([1, 2, 3], x=1)
    with pytest.raises(ValueError, match=r"plot\(\) with multiple groups"):
        plt.plot([1, 2, 3], [1, 2, 3], [2, 3, 4], [2, 3, 4], label=['1', '2'])
    with pytest.raises(ValueError, match="x and y must have same first"):
        plt.plot([1, 2, 3], [1])
    with pytest.raises(ValueError, match="x and y can be no greater than"):
        plt.plot(np.ones((2, 2, 2)))
    with pytest.raises(ValueError, match="Using arbitrary long args with"):
        plt.plot("a", "b", "c", "d", data={"a": 2})

