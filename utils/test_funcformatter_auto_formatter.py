
def test_funcformatter_auto_formatter():
    def _formfunc(x, pos):
        return ''

    ax = plt.figure().subplots()

    assert ax.xaxis.isDefault_majfmt
    assert ax.xaxis.isDefault_minfmt
    assert ax.yaxis.isDefault_majfmt
    assert ax.yaxis.isDefault_minfmt

    ax.xaxis.set_major_formatter(_formfunc)

    assert not ax.xaxis.isDefault_majfmt
    assert ax.xaxis.isDefault_minfmt
    assert ax.yaxis.isDefault_majfmt
    assert ax.yaxis.isDefault_minfmt

    targ_funcformatter = mticker.FuncFormatter(_formfunc)

    assert isinstance(ax.xaxis.get_major_formatter(),
                      mticker.FuncFormatter)

    assert ax.xaxis.get_major_formatter().func == targ_funcformatter.func

