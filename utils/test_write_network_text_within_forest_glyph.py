
def test_write_network_text_within_forest_glyph():
    g = nx.DiGraph()
    g.add_nodes_from([1, 2, 3, 4])
    g.add_edge(2, 4)
    lines = []
    write = lines.append
    nx.write_network_text(g, path=write, end="")
    nx.write_network_text(g, path=write, ascii_only=True, end="")
    text = "\n".join(lines)
    target = dedent(
        """
        ╟── 1
        ╟── 2
        ╎   └─╼ 4
        ╙── 3
        +-- 1
        +-- 2
        :   L-> 4
        +-- 3
        """
    ).strip()
    assert text == target

