
def randomize_graph_initializer(graph):
    for i_tensor in graph.initializer:
        array = numpy_helper.to_array(i_tensor)
        # TODO: need to find a better way to differentiate shape data and weights.
        if array.size > SIZE_THRESHOLD:
            random_array = np.random.uniform(array.min(), array.max(), size=array.shape).astype(array.dtype)
            o_tensor = numpy_helper.from_array(random_array, i_tensor.name)
            i_tensor.CopyFrom(o_tensor)

