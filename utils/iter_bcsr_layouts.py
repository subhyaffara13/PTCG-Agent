
def iter_bcsr_layouts(
    shape: Sequence[int], min_n_batch=0
) -> Iterator[SparseLayout]:
  n_sparse = 2
  for n_batch in range(min_n_batch, len(shape) - 1):
    n_dense = len(shape) - n_sparse - n_batch
    yield SparseLayout(n_batch=n_batch, n_sparse=n_sparse, n_dense=n_dense)

