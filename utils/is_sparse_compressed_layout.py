
def is_sparse_compressed_layout(layout: torch.layout) -> bool:
    return layout in {
        torch.sparse_csr,
        torch.sparse_csc,
        torch.sparse_bsr,
        torch.sparse_bsc,
    }

