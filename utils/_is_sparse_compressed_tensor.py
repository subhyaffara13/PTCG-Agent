
def _is_sparse_compressed_tensor(obj: torch.Tensor):
    return obj.layout in {
        torch.sparse_csr,
        torch.sparse_csc,
        torch.sparse_bsr,
        torch.sparse_bsc,
    }

