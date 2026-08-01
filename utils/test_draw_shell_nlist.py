
def test_draw_shell_nlist(subplots, tmp_path):
    fig, _ = subplots
    nlist = [list(range(4)), list(range(4, 10)), list(range(10, 14))]
    nx.draw_shell(barbell, nlist=nlist)
    fig.savefig(tmp_path / "test.ps")

