
def test_predecessors():
    SP_res = {True: directed_SP,
              False: undirected_SP}
    pred_res = {True: directed_pred,
                False: undirected_pred}

    def check(method, directed):
        SP, pred = shortest_path(directed_G, method, directed=directed,
                                 overwrite=False,
                                 return_predecessors=True)
        assert_array_almost_equal(SP, SP_res[directed])
        assert_array_almost_equal(pred, pred_res[directed])

    for method in methods:
        for directed in (True, False):
            check(method, directed)

