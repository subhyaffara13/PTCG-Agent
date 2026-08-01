
def test_is_minimal_d_separator_checks_dsep():
    """Test that is_minimal_d_separator checks for d-separation as well."""
    g = nx.DiGraph()
    g.add_edges_from(
        [
            ("A", "B"),
            ("A", "E"),
            ("B", "C"),
            ("B", "D"),
            ("D", "C"),
            ("D", "F"),
            ("E", "D"),
            ("E", "F"),
        ]
    )

    assert not nx.is_d_separator(g, {"C"}, {"F"}, {"D"})

    # since {'D'} and {} are not d-separators, we return false
    assert not nx.is_minimal_d_separator(g, "C", "F", {"D"})
    assert not nx.is_minimal_d_separator(g, "C", "F", set())

