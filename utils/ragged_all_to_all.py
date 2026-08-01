
def ragged_all_to_all(
    operand, output, input_offsets, send_sizes, output_offsets, recv_sizes, *,
    axis_name, axis_index_groups = None):
  """Ragged version of :func:`all_to_all` collective.

  We say data are "ragged" when they can be represented as a list of arrays
  whose shapes differ only in the size of the leading axis. For example, these
  data are ragged, comprising four component arrays::

    ragged_data = [jnp.arange(3), jnp.arange(1), jnp.arange(4), jnp.arange(1)]

  We often instead want a contiguous representation, e.g. for batching. But
  because the shapes of the components differ, we can't apply ``jnp.stack`` to
  represent these data by a single rectangular array with the leading axis
  indexing the component arrays. So instead of stacking, we concatenate along
  the leading axis and keep track of offsets and sizes.

  That is, we can represent ragged data contiguously using a triple of dense
  arrays ``(data, offsets, sizes)``:

    * ``data``: the concatenated component arrays,
    * ``offsets``: 1D array of indices into the leading axis of ``data``
      indicating where the data for each component array begins,
    * ``sizes``: 1D array of sizes of the leading axis of each component array.

  We refer to this triple as a ragged array. (Offsets can't be computed from
  sizes in general to allow for internal padding.)

  For example::

    data: f32[8,3] = jnp.array([
        [a,b,c], [d,e,f], [g,h,i], [j,k,l], [m,n,o], [p,q,r], [s,t,u], [v,w,x],
    ])
    offsets: i32[3] = jnp.array([0, 1, 4])
    sizes: i32[3] = jnp.array([1, 3, 4])

    # To extract the first component array, of type f32[1,3]
    data[offsets[0]:offsets[0]+sizes[0]]

    # To extract the second component array, of type f32[3,3]
    data[offsets[1]:offsets[1]+sizes[1]]

    # To extract the third component array, of type f32[4,3]
    data[offsets[2]:offsets[2]+sizes[2]]

  The ``ragged_all_to_all`` collective operation communicates slices of ragged
  arrays between devices. Each caller is both a sender and a receiver. The
  ``input_offsets`` and ``send_sizes`` arguments indicate the slices of the
  caller's ``operand`` to be sent. Received results are returned in an array
  that has the same value of the argument ``output`` except with received values
  written at some slices. The ``output_offsets`` argument does *not* indicate
  the offsets at which all the received results are written; instead,
  ``output_offsets`` indicates the offsets at which the *sent* slices are
  written on their corresponding receivers. The sizes of received slices are
  indicated by ``recv_sizes``. See below for details.

  The arrays ``input_offsets``, ``send_sizes``,``output_offsets``, and
  ``recv_sizes`` must all be the same length, and that length must be divisible
  by the size of the mapped axis ``axis_name``. Moreover, ``send_sizes`` and
  ``recv_sizes`` must satisfy::

    jnp.all(send_sizes == jax.lax.all_to_all(recv_sizes, axis_name, 0, 0, tiled=True))

  Specifically, given a call::

    result = ragged_all_to_all(operand, output, input_offsets, send_sizes,
                               output_offsets, recv_sizes, axis_name)

  the caller sends data like::

    assert len(input_offsets) == len(send_sizes) == len(output_offsets) == len(recv_sizes)
    N = len(input_offsets)
    slices_per_device, leftover = divmod(N, lax.axis_size(axis_name))
    assert not leftover

    for i in range(N):
      dst_idx = i // slices_per_device
      SEND(data=operand[input_offsets[i]:input_offsets[i]+send_sizes[i]],
           axis_name=axis_name, to_axis_index=dst_idx)

  and receives data in ``result`` like::

    result = output
    output_offsets_ = jax.lax.all_to_all(output_offsets, axis_name, 0, 0, tiled=True)
    for i in range(N):
      src_idx = i // slices_per_device
      result = result.at[output_offsets_[i]:output_offsets_[i]+recv_sizes[i]
                    ].set(RECEIVE(axis_name=axis_name, from_axis_index=src_idx))

  where ``SEND`` and ``RECEIVE`` are pseudocode. Notice that a caller's local
  ``output_offsets`` does not indicate the offsets at which its local ``result``
  is updated; instead, it indicates where the corresponding sent slices are
  written on their destination instances. To compute the local offsets at which
  received data are written, we apply an ``all_to_all`` on ``output_offsets``.

  For example, if we apply a ``ragged_all_to_all`` along an axis of size 2, with
  these arguments in each mapped function instance::

    axis index 0:
      operand = [1, 2, 2]
      output = [0, 0, 0, 0]
      input_offsets = [0, 1]
      send_sizes = [1, 2]
      output_offsets = [0, 0]
      recv_sizes = [1, 1]

    axis index 1:
      operand = [3, 4, 0]
      output = [0, 0, 0, 0]
      input_offsets = [0, 1]
      send_sizes = [1, 1]
      output_offsets = [1, 2]
      recv_sizes = [2, 1]

  then::

    axis index 0:
      result = [1, 3, 0, 0]

    axis index 1:
      result = [2, 2, 4, 0]

  Args:
    operand: data array of shape (N, A, B, ...) representing concatenated
      (possibly padded) ragged data to be sent.
    output: data array of shape (M, A, B, ...) to update with received data.
    input_offsets: 1D integer array of shape (K,) representing the offsets of
      leading-axis slices into ``operand`` to be sent.
    send_sizes: 1D integer array array of shape (K,) representing the sizes of
      leading-axis slices into ``operand`` to be sent.
    output_offsets: 1D integer array of shape (K,) representing where the
      corresponding sent data is written on each corresponding receiver.
    recv_sizes: 1D integer array of shape (K,) representing sizes of
      leading-axis slices into ``output`` to update with received data.
    axis_name: name of the mapped axis over which to perform the communication.
    axis_index_groups: optional list of lists containing axis indices (e.g. for
      an axis of size 4, [[0, 1], [2, 3]] would run ragged all to all over the
      first two and last two replicas). Groups must cover all axis indices
      exactly once, and all groups must be the same size. Otherwise, the
      behavior is undefined.

  Returns:
    Array of shape (M, A, B, ...) with the same value as the ``output`` except
    with received data written into slices starting at
    ``all_to_all(output_offsets, axis_name, 0, 0, tiled=True)`` and with size
    ``recv_sizes``.
  """

  if not isinstance(axis_name, (tuple, list)):
    axis_name = (axis_name,)

  axis_index_groups = _canonicalize_axis_index_groups(axis_index_groups)
  return ragged_all_to_all_p.bind(operand, output, input_offsets, send_sizes,
                                  output_offsets, recv_sizes,
                                  axis_name=axis_name,
                                  axis_index_groups=axis_index_groups)

