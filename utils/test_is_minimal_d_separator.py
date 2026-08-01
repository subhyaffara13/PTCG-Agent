
def test_is_minimal_d_separator(
    large_collider_graph,
    chain_and_fork_graph,
    no_separating_set_graph,
    large_no_separating_set_graph,
    collider_trek_graph,
):
    # Case 1:
    # create a graph A -> B <- C
    # B -> D -> E;
    # B -> F;
    # G -> E;
    assert not nx.is_d_separator(large_collider_graph, {"B"}, {"E"}, set())

    # minimal set of the corresponding graph
    # for B and E should be (D,)
    Zmin = nx.find_minimal_d_separator(large_collider_graph, "B", "E")
    # check that the minimal d-separator is a d-separating set
    assert nx.is_d_separator(large_collider_graph, "B", "E", Zmin)
    # the minimal separating set should also pass the test for minimality
    assert nx.is_minimal_d_separator(large_collider_graph, "B", "E", Zmin)
    # function should also work with set arguments
    assert nx.is_minimal_d_separator(large_collider_graph, {"A", "B"}, {"G", "E"}, Zmin)
    assert Zmin == {"D"}

    # Case 2:
    # create a graph A -> B -> C
    # B -> D -> C;
    assert not nx.is_d_separator(chain_and_fork_graph, {"A"}, {"C"}, set())
    Zmin = nx.find_minimal_d_separator(chain_and_fork_graph, "A", "C")

    # the minimal separating set should pass the test for minimality
    assert nx.is_minimal_d_separator(chain_and_fork_graph, "A", "C", Zmin)
    assert Zmin == {"B"}
    Znotmin = Zmin.union({"D"})
    assert not nx.is_minimal_d_separator(chain_and_fork_graph, "A", "C", Znotmin)

    # Case 3:
    # create a graph A -> B

    # there is no m-separating set between A and B at all, so
    # no minimal m-separating set can exist
    assert not nx.is_d_separator(no_separating_set_graph, {"A"}, {"B"}, set())
    assert nx.find_minimal_d_separator(no_separating_set_graph, "A", "B") is None

    # Case 4:
    # create a graph A -> B with A <- C -> B

    # there is no m-separating set between A and B at all, so
    # no minimal m-separating set can exist
    # however, the algorithm will initially propose C as a
    # minimal (but invalid) separating set
    assert not nx.is_d_separator(large_no_separating_set_graph, {"A"}, {"B"}, {"C"})
    assert nx.find_minimal_d_separator(large_no_separating_set_graph, "A", "B") is None

    # Test `included` and `excluded` args
    # create graph A -> B <- C -> D
    assert nx.find_minimal_d_separator(collider_trek_graph, "A", "D", included="B") == {
        "B",
        "C",
    }
    assert (
        nx.find_minimal_d_separator(
            collider_trek_graph, "A", "D", included="B", restricted="B"
        )
        is None
    )

