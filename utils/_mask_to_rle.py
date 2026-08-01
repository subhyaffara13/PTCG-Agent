
def _mask_to_rle(input_mask: "torch.Tensor"):
    """
    Encodes masks the run-length encoding (RLE), in the format expected by pycoco tools.
    """
    # Put in fortran order and flatten height and width
    batch_size, height, width = input_mask.shape
    input_mask = input_mask.permute(0, 2, 1).flatten(1)

    # Compute change indices
    diff = input_mask[:, 1:] ^ input_mask[:, :-1]
    change_indices = diff.nonzero()

    # Encode run length
    out = []
    for i in range(batch_size):
        cur_idxs = change_indices[change_indices[:, 0] == i, 1] + 1
        if len(cur_idxs) == 0:
            # No changes => either all 0 or all 1
            # If the entire mask is 0, RLE is [height*width] or if the entire mask is 1, RLE is [0, height*width].
            if input_mask[i, 0] == 0:
                out.append({"size": [height, width], "counts": [height * width]})
            else:
                out.append({"size": [height, width], "counts": [0, height * width]})
            continue
        btw_idxs = cur_idxs[1:] - cur_idxs[:-1]
        counts = [] if input_mask[i, 0] == 0 else [0]
        counts += [cur_idxs[0].item()] + btw_idxs.tolist() + [height * width - cur_idxs[-1].item()]
        out.append({"size": [height, width], "counts": counts})
    return out


def _mask_to_rle(input_mask: "torch.Tensor"):
    """
    Encodes masks the run-length encoding (RLE), in the format expected by pycoco tools.
    """
    # Put in fortran order and flatten height and width
    batch_size, height, width = input_mask.shape
    input_mask = input_mask.permute(0, 2, 1).flatten(1)

    # Compute change indices
    diff = input_mask[:, 1:] ^ input_mask[:, :-1]
    change_indices = diff.nonzero()

    # Encode run length
    out = []
    for i in range(batch_size):
        cur_idxs = change_indices[change_indices[:, 0] == i, 1] + 1
        if len(cur_idxs) == 0:
            # No changes => either all 0 or all 1
            # If the entire mask is 0, RLE is [height*width] or if the entire mask is 1, RLE is [0, height*width].
            if input_mask[i, 0] == 0:
                out.append({"size": [height, width], "counts": [height * width]})
            else:
                out.append({"size": [height, width], "counts": [0, height * width]})
            continue
        btw_idxs = cur_idxs[1:] - cur_idxs[:-1]
        counts = [] if input_mask[i, 0] == 0 else [0]
        counts += [cur_idxs[0].item()] + btw_idxs.tolist() + [height * width - cur_idxs[-1].item()]
        out.append({"size": [height, width], "counts": counts})
    return out


def _mask_to_rle(input_mask: "torch.Tensor"):
    """
    Encodes masks the run-length encoding (RLE), in the format expected by pycoco tools.
    """
    # Put in fortran order and flatten height and width
    batch_size, height, width = input_mask.shape
    input_mask = input_mask.permute(0, 2, 1).flatten(1)

    # Compute change indices
    diff = input_mask[:, 1:] ^ input_mask[:, :-1]
    change_indices = diff.nonzero()

    # Encode run length
    out = []
    for i in range(batch_size):
        cur_idxs = change_indices[change_indices[:, 0] == i, 1] + 1
        if len(cur_idxs) == 0:
            # No changes => either all 0 or all 1
            # If the entire mask is 0, RLE is [height*width] or if the entire mask is 1, RLE is [0, height*width].
            if input_mask[i, 0] == 0:
                out.append({"size": [height, width], "counts": [height * width]})
            else:
                out.append({"size": [height, width], "counts": [0, height * width]})
            continue
        btw_idxs = cur_idxs[1:] - cur_idxs[:-1]
        counts = [] if input_mask[i, 0] == 0 else [0]
        counts += [cur_idxs[0].item()] + btw_idxs.tolist() + [height * width - cur_idxs[-1].item()]
        out.append({"size": [height, width], "counts": counts})
    return out


def _mask_to_rle(input_mask: "torch.Tensor"):
    """
    Encodes masks the run-length encoding (RLE), in the format expected by pycoco tools.
    """
    # Put in fortran order and flatten height and width
    batch_size, height, width = input_mask.shape
    input_mask = input_mask.permute(0, 2, 1).flatten(1)

    # Compute change indices
    diff = input_mask[:, 1:] ^ input_mask[:, :-1]
    change_indices = diff.nonzero()

    # Encode run length
    out = []
    for i in range(batch_size):
        cur_idxs = change_indices[change_indices[:, 0] == i, 1] + 1
        if len(cur_idxs) == 0:
            # No changes => either all 0 or all 1
            # If the entire mask is 0, RLE is [height*width] or if the entire mask is 1, RLE is [0, height*width].
            if input_mask[i, 0] == 0:
                out.append({"size": [height, width], "counts": [height * width]})
            else:
                out.append({"size": [height, width], "counts": [0, height * width]})
            continue
        btw_idxs = cur_idxs[1:] - cur_idxs[:-1]
        counts = [] if input_mask[i, 0] == 0 else [0]
        counts += [cur_idxs[0].item()] + btw_idxs.tolist() + [height * width - cur_idxs[-1].item()]
        out.append({"size": [height, width], "counts": counts})
    return out

