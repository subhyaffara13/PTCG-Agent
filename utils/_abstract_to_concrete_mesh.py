
def _abstract_to_concrete_mesh(abstract_mesh, device_assignment):
  np_dev = np.vectorize(lambda i: device_assignment[i],
                        otypes=[object])(np.arange(len(device_assignment)))
  return Mesh(np_dev.reshape(abstract_mesh.axis_sizes),
              abstract_mesh.axis_names, axis_types=abstract_mesh.axis_types)

