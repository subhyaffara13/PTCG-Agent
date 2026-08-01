
def test_new_functions_untested_here():
    #This tests whether any new code has arrived that isn't in the list above.

    # funcs tested individually outside of check_these_functions
    handled = ["shortest_path", "construct_dist_matrix", "reconstruct_path",
               "csgraph_from_dense", "csgraph_from_masked", "csgraph_masked_from_dense"]

    # look for functions that should be tested
    functions = [fname for fname in dir(csgraph_subpackage)
                 if fname[0] != "_"
                 if not fname.endswith("Error")
                 if not fname.startswith("test")
                 if fname not in handled]

    checked_funcs = [x[0].__name__ for x in check_these_functions]
    for func in functions:
        if func not in checked_funcs:
            msg = (f'function "{func}" in csgraph is not tested. '
                   'It should be added to the `check_these_functions` list above or '
                   'handled separately if its signature has many required parameters')
            raise ValueError(msg)

