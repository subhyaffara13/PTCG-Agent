
def test_markerfacecolor_fillstyle():
    """Test that markerfacecolor does not override fillstyle='none'."""
    l, = plt.plot([1, 3, 2], marker=MarkerStyle('o', fillstyle='none'),
                  markerfacecolor='red')
    assert l.get_fillstyle() == 'none'
    assert l.get_markerfacecolor() == 'none'

