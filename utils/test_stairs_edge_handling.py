
def test_stairs_edge_handling(fig_test, fig_ref):
    # Test
    test_ax = fig_test.add_subplot()
    test_ax.stairs([1, 2, 3], color='red', fill=True)

    # Ref
    ref_ax = fig_ref.add_subplot()
    st = ref_ax.stairs([1, 2, 3], fill=True)
    st.set_color('red')

