
def _pad(items, key, padding_value, padding_side):
    batch_size = len(items)
    if isinstance(items[0][key], torch.Tensor):
        # Others include `attention_mask` etc...
        shape = items[0][key].shape
        dim = items[0][key].ndim
        if dim == 1:
            # We have a list of 1-dim torch tensors, which can be stacked without padding
            return torch.cat([item[key] for item in items], dim=0)
        if key in ["pixel_values", "image"]:
            # This is probable image so padding shouldn't be necessary
            # B, C, H, W
            return torch.cat([item[key] for item in items], dim=0)
        elif dim == 4 and key == "input_features":
            # this is probably a mel spectrogram batched
            return torch.cat([item[key] for item in items], dim=0)
        max_length = max(item[key].shape[1] for item in items)
        min_length = min(item[key].shape[1] for item in items)
        dtype = items[0][key].dtype

        if dim == 2 and max_length == min_length:
            # Bypass for `ImageGPT` which doesn't provide a padding value, yet
            # we can consistently pad since the size should be matching
            return torch.cat([item[key] for item in items], dim=0)
        else:
            tensor = torch.full([batch_size, max_length] + list(shape[2:]), fill_value=padding_value, dtype=dtype)

        for i, item in enumerate(items):
            if padding_side == "left":
                tensor[i, -len(item[key][0]) :] = item[key][0]
            else:
                tensor[i, : len(item[key][0])] = item[key][0]

        return tensor
    else:
        return [item[key] for item in items]


def _pad(text, width):
    t = str(text)
    pad = max(0, width - len(_strip_ansi(t)))
    return t + " " * pad


def _pad(arr, pads, pad_value):
  out = np.pad(arr, np.maximum(0, pads), mode='constant',
                constant_values=pad_value).astype(arr.dtype)
  slices = tuple(_slice(abs(lo) if lo < 0 else 0, hi % dim if hi < 0 else None)
                 for (lo, hi), dim in zip(pads, np.shape(arr)))
  return out[slices]


def _pad(array: ArrayLike, pad_width: PadValueLike[int], mode: str,
         constant_values: ArrayLike, stat_length: PadValueLike[int],
         end_values: PadValueLike[ArrayLike], reflect_type: str):
  array = asarray(array)
  nd = np.ndim(array)

  if nd == 0:
    return array

  stat_funcs: dict[str, PadStatFunc] = {
      "maximum": reductions.amax,
      "minimum": reductions.amin,
      "mean": reductions.mean,
      "median": reductions.median
  }

  pad_width = _broadcast_to_pairs(pad_width, nd, "pad_width")
  pad_width_arr = np.array(pad_width)
  if pad_width_arr.shape != (nd, 2):
    raise ValueError(f"Expected pad_width to have shape {(nd, 2)}; got {pad_width_arr.shape}.")

  if np.any(pad_width_arr < 0):
    raise ValueError("index can't contain negative values")

  if mode == "constant":
    return _pad_constant(array, pad_width, asarray(constant_values))

  elif mode == "wrap":
    return _pad_wrap(array, pad_width)

  elif mode in ("symmetric", "reflect"):
    return _pad_symmetric_or_reflect(array, pad_width, str(mode), reflect_type)

  elif mode == "edge":
    return _pad_edge(array, pad_width)

  elif mode == "linear_ramp":
    end_values = _broadcast_to_pairs(end_values, nd, "end_values")
    return _pad_linear_ramp(array, pad_width, end_values)

  elif mode in stat_funcs:
    if stat_length is not None:
      stat_length = _broadcast_to_pairs(stat_length, nd, "stat_length")
    return _pad_stats(array, pad_width, stat_length, stat_funcs[str(mode)])

  elif mode == "empty":
    return _pad_empty(array, pad_width)

  else:
    assert False, ("Should not be reached since pad already handled unsupported and"
                   "not implemented modes")

