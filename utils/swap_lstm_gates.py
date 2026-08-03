import math


def swap_lstm_gates(weights, input_size, hidden_size, num_layers, bidirectional):
  """Swaps the weights for the input and output gates for an LSTM model."""
  weights = jnp.asarray(weights)  # Ensure weights are JAX arrays
  flat_shapes = _get_params_shapes_in_lstm(input_size, hidden_size, num_layers, bidirectional)
  num_directions = 2 if bidirectional else 1

  w_offsets = 0
  for l in range(num_layers):
    for direction in range(num_directions):
      # Iterate through all weight and bias gate names to swap gates in both weights and biases
      for gate_name in ["W_ih", "W_hh", "b_ih", "b_hh"]:
        shape = flat_shapes.pop(0)  # Get the current shape and remove it from the list
        num_elems = math.prod(shape)
        matrix = weights[w_offsets:w_offsets + num_elems].reshape(shape)

        # Swap between the input and output gates (third and fourth gates)
        gates = jnp.split(matrix, 4, axis=0)
        swapped_matrix = jnp.concatenate([gates[0], gates[1], gates[3], gates[2]], axis=0)

        # Update the weights with swapped matrix
        weights = weights.at[w_offsets:w_offsets + num_elems].set(swapped_matrix.flatten())
        w_offsets += num_elems

  return weights

