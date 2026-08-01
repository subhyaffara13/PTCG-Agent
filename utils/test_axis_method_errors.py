
def test_axis_method_errors():
    ax = plt.gca()
    with pytest.raises(ValueError, match="unknown value for which: 'foo'"):
        ax.get_xaxis_transform('foo')
    with pytest.raises(ValueError, match="unknown value for which: 'foo'"):
        ax.get_yaxis_transform('foo')
    with pytest.raises(TypeError, match="Cannot supply both positional and"):
        ax.set_prop_cycle('foo', label='bar')
    with pytest.raises(ValueError, match="argument must be among"):
        ax.set_anchor('foo')
    with pytest.raises(ValueError, match="scilimits must be a sequence"):
        ax.ticklabel_format(scilimits=1)
    with pytest.raises(TypeError, match="Specifying 'loc' is disallowed"):
        ax.set_xlabel('foo', loc='left', x=1)
    with pytest.raises(TypeError, match="Specifying 'loc' is disallowed"):
        ax.set_ylabel('foo', loc='top', y=1)
    with pytest.raises(TypeError, match="Cannot pass both 'left'"):
        ax.set_xlim(left=0, xmin=1)
    with pytest.raises(TypeError, match="Cannot pass both 'right'"):
        ax.set_xlim(right=0, xmax=1)
    with pytest.raises(TypeError, match="Cannot pass both 'bottom'"):
        ax.set_ylim(bottom=0, ymin=1)
    with pytest.raises(TypeError, match="Cannot pass both 'top'"):
        ax.set_ylim(top=0, ymax=1)

