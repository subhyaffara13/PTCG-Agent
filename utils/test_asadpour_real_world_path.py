
def test_asadpour_real_world_path():
    """
    This test uses airline prices between the six largest cities in the US. This
    time using a path, not a cycle.

        * New York City -> JFK
        * Los Angeles -> LAX
        * Chicago -> ORD
        * Houston -> IAH
        * Phoenix -> PHX
        * Philadelphia -> PHL

    Flight prices from August 2021 using Delta or American airlines to get
    nonstop flight. The brute force solution found the optimal tour to cost $872
    """
    np = pytest.importorskip("numpy")
    pytest.importorskip("scipy")

    G_array = np.array(
        [
            # JFK  LAX  ORD  IAH  PHX  PHL
            [0, 243, 199, 208, 169, 183],  # JFK
            [277, 0, 217, 123, 127, 252],  # LAX
            [297, 197, 0, 197, 123, 177],  # ORD
            [303, 169, 197, 0, 117, 117],  # IAH
            [257, 127, 160, 117, 0, 319],  # PHX
            [183, 332, 217, 117, 319, 0],  # PHL
        ]
    )

    node_list = ["JFK", "LAX", "ORD", "IAH", "PHX", "PHL"]

    expected_paths = [
        ["ORD", "PHX", "LAX", "IAH", "PHL", "JFK"],
        ["JFK", "PHL", "IAH", "ORD", "PHX", "LAX"],
    ]

    G = nx.from_numpy_array(G_array, nodelist=node_list, create_using=nx.DiGraph)

    path = nx_app.traveling_salesman_problem(
        G, weight="weight", cycle=False, method=nx_app.asadpour_atsp, seed=56
    )

    assert path in expected_paths

