
def test_display_arg_handling_node_color(param_name, param_value, expected):
    G = nx.path_graph(4)
    nx.set_node_attributes(G, "#00FF00", "color")
    canvas = plt.figure().add_subplot(111)
    nx.display(G, canvas=canvas, **{param_name: param_value})
    assert mpl.colors.same_color(canvas.get_children()[0].get_edgecolors()[0], expected)
    plt.close()

