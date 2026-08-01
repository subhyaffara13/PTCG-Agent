
def iter_sparse_layouts(
    shape: Sequence[int], min_n_batch=0
) -> Iterator[SparseLayout]:
  for n_batch in range(min_n_batch, len(shape) + 1):
    for n_dense in range(len(shape) + 1 - n_batch):
      n_sparse = len(shape) - n_batch - n_dense
      yield SparseLayout(n_batch=n_batch, n_sparse=n_sparse, n_dense=n_dense)

