
def fill_holes_in_mask_scores(mask, max_area, fill_holes=True, remove_sprinkles=True):
    """
    A post processor to fill small holes in mask scores with area under `max_area`.
    Holes are those small connected components in either background or foreground.

    Note that it relies on the "cc_torch" package to find connected components fast. You can
    install it via the following command (`TORCH_CUDA_ARCH_LIST=8.0` is for A100 GPUs):
    ```
    pip uninstall -y cc_torch; TORCH_CUDA_ARCH_LIST=8.0 9.0 pip install git+https://github.com/ronghanghu/cc_torch
    ```
    Otherwise, it will fallback to a slightly slower triton implementation, or skimage if the tensor is on cpu
    """

    if max_area <= 0:
        return mask  # nothing to fill in this case

    if fill_holes:
        # We remove small connected components in background by changing them to foreground
        # with a small positive mask score (0.1).
        mask_bg = mask <= 0
        bg_area_thresh = max_area
        _, areas_bg = _get_connected_components_with_padding(mask_bg)
        small_components_bg = mask_bg & (areas_bg <= bg_area_thresh)
        mask = torch.where(small_components_bg, 0.1, mask)

    if remove_sprinkles:
        # We remove small connected components in foreground by changing them to background
        # with a small negative mask score (-0.1). Here we only remove connected components
        # whose areas are under both `max_area` and half of the entire mask's area. This
        # removes sprinkles while avoids filtering out tiny objects that we want to track.
        mask_fg = mask > 0
        fg_area_thresh = torch.sum(mask_fg, dim=(2, 3), keepdim=True, dtype=torch.int32)
        fg_area_thresh.floor_divide_(2).clamp_(max=max_area)
        _, areas_fg = _get_connected_components_with_padding(mask_fg)
        small_components_fg = mask_fg & (areas_fg <= fg_area_thresh)
        mask = torch.where(small_components_fg, -0.1, mask)
    return mask

