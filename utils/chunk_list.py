
def chunk_list(lst, nchunks):
    return [lst[i::nchunks] for i in range(nchunks)]

