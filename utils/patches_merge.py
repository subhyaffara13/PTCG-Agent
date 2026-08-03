import math


def patches_merge(
    patches: "torch.Tensor",
    positions_xy: "torch.Tensor",
    length: int,
) -> tuple["torch.Tensor", "torch.Tensor"]:
    """Merge k×k groups of small patches into larger patches.

    Given `L` input patches of dimension `D = patch_size² × 3`, merge groups of
    `k×k` spatially adjacent patches into `length` output patches of dimension
    `(k × patch_size)² × 3`. The spatial grouping is determined by integer-dividing
    the XY positions by `k`.

    Args:
        patches: (*, L, D) — input patches.
        positions_xy: (*, L, 2) — integer XY positions for each patch (-1 for padding).
        length: target number of output patches. Must satisfy L = length × k².

    Returns:
        merged_patches: (*, length, k²×D) — merged patch features.
        merged_positions: (*, length, 2) — new XY positions for merged patches.
    """
    patch_size = math.isqrt(patches.shape[-1] // 3)
    if patches.shape[-1] != patch_size * patch_size * 3:
        raise ValueError(f"Patch dimension {patches.shape[-1]} is not a valid `patch_size * patch_size * 3`")

    k = math.isqrt(patches.shape[-2] // length)
    if k * k * length != patches.shape[-2]:
        raise ValueError(f"Cannot merge {patches.shape} to {length}")

    # Compute target ordering for reordering patches into kernel-grouped order.
    # This ensures patches within each k×k kernel are contiguous.
    max_x = positions_xy[..., 0].max(dim=-1, keepdim=True)[0] + 1
    kernel_idxs = torch.div(positions_xy, k, rounding_mode="floor")
    num_patches_from_top_left = k * k * kernel_idxs[..., 0] + k * max_x * kernel_idxs[..., 1]

    position_within_kernel = torch.remainder(positions_xy, k)
    num_patches_from_top_left_of_kernel = position_within_kernel[..., 0] + position_within_kernel[..., 1] * k
    target_ordering = num_patches_from_top_left_of_kernel + num_patches_from_top_left

    # Reorder patches by computing the inverse permutation via argsort,
    # then gathering patches into kernel-grouped order.
    perm = target_ordering.long().argsort(dim=-1)  # inverse permutation
    # Expand perm indices to match patch feature dimension for gathering
    perm_expanded = perm.unsqueeze(-1).expand_as(patches)
    kernel_ordered_patches = patches.gather(-2, perm_expanded)

    batch_shape = patches.shape[:-2]

    # Reshape: (*, length*k*k, patch_size*patch_size*3) → (*, length, (k*patch_size)*(k*patch_size)*3)
    kernel_ordered_patches = kernel_ordered_patches.reshape(*batch_shape, length, k * k, patch_size, patch_size, 3)
    # Rearrange (l, a*b, p, q, c) → (l, a*p, b*q, c)
    kernel_ordered_patches = kernel_ordered_patches.reshape(*batch_shape, length, k, k, patch_size, patch_size, 3)
    kernel_ordered_patches = kernel_ordered_patches.permute(
        *range(len(batch_shape)), -6, -5, -3, -4, -2, -1
    )  # (..., l, k, p, k, q, c)
    merged_patches = kernel_ordered_patches.reshape(*batch_shape, length, k * patch_size * k * patch_size * 3)

    # Compute new positions for merged patches
    perm_pos = perm.unsqueeze(-1).expand_as(positions_xy)
    kernel_ordered_positions = positions_xy.float().gather(-2, perm_pos.long())

    # Handle padding: preserve -1 positions
    padding = (positions_xy == -1).all(dim=-1, keepdim=True)  # (..., L, 1)
    kernel_ordered_positions = kernel_ordered_positions * (~padding).float() + positions_xy.float() * padding.float()

    # Reshape positions and take min within each kernel to get the merged position
    kernel_ordered_positions = kernel_ordered_positions.reshape(*batch_shape, length, k * k, 2)
    new_positions = torch.div(kernel_ordered_positions, k, rounding_mode="floor")
    # For each merged patch, take the minimum position across the kernel
    new_positions = new_positions.min(dim=-2)[0].to(torch.long)

    return merged_patches, new_positions


def patches_merge(
    patches: "torch.Tensor",
    positions_xy: "torch.Tensor",
    length: int,
) -> tuple["torch.Tensor", "torch.Tensor"]:
    """Merge k×k groups of small patches into larger patches.

    Given `L` input patches of dimension `D = patch_size² × 3`, merge groups of
    `k×k` spatially adjacent patches into `length` output patches of dimension
    `(k × patch_size)² × 3`. The spatial grouping is determined by integer-dividing
    the XY positions by `k`.

    Args:
        patches: (*, L, D) — input patches.
        positions_xy: (*, L, 2) — integer XY positions for each patch (-1 for padding).
        length: target number of output patches. Must satisfy L = length × k².

    Returns:
        merged_patches: (*, length, k²×D) — merged patch features.
        merged_positions: (*, length, 2) — new XY positions for merged patches.
    """
    patch_size = math.isqrt(patches.shape[-1] // 3)
    if patches.shape[-1] != patch_size * patch_size * 3:
        raise ValueError(f"Patch dimension {patches.shape[-1]} is not a valid `patch_size * patch_size * 3`")

    k = math.isqrt(patches.shape[-2] // length)
    if k * k * length != patches.shape[-2]:
        raise ValueError(f"Cannot merge {patches.shape} to {length}")

    # Compute target ordering for reordering patches into kernel-grouped order.
    # This ensures patches within each k×k kernel are contiguous.
    max_x = positions_xy[..., 0].max(dim=-1, keepdim=True)[0] + 1
    kernel_idxs = torch.div(positions_xy, k, rounding_mode="floor")
    num_patches_from_top_left = k * k * kernel_idxs[..., 0] + k * max_x * kernel_idxs[..., 1]

    position_within_kernel = torch.remainder(positions_xy, k)
    num_patches_from_top_left_of_kernel = position_within_kernel[..., 0] + position_within_kernel[..., 1] * k
    target_ordering = num_patches_from_top_left_of_kernel + num_patches_from_top_left

    # Reorder patches by computing the inverse permutation via argsort,
    # then gathering patches into kernel-grouped order.
    perm = target_ordering.long().argsort(dim=-1)  # inverse permutation
    # Expand perm indices to match patch feature dimension for gathering
    perm_expanded = perm.unsqueeze(-1).expand_as(patches)
    kernel_ordered_patches = patches.gather(-2, perm_expanded)

    batch_shape = patches.shape[:-2]

    # Reshape: (*, length*k*k, patch_size*patch_size*3) → (*, length, (k*patch_size)*(k*patch_size)*3)
    kernel_ordered_patches = kernel_ordered_patches.reshape(*batch_shape, length, k * k, patch_size, patch_size, 3)
    # Rearrange (l, a*b, p, q, c) → (l, a*p, b*q, c)
    kernel_ordered_patches = kernel_ordered_patches.reshape(*batch_shape, length, k, k, patch_size, patch_size, 3)
    kernel_ordered_patches = kernel_ordered_patches.permute(
        *range(len(batch_shape)), -6, -5, -3, -4, -2, -1
    )  # (..., l, k, p, k, q, c)
    merged_patches = kernel_ordered_patches.reshape(*batch_shape, length, k * patch_size * k * patch_size * 3)

    # Compute new positions for merged patches
    perm_pos = perm.unsqueeze(-1).expand_as(positions_xy)
    kernel_ordered_positions = positions_xy.float().gather(-2, perm_pos.long())

    # Handle padding: preserve -1 positions
    padding = (positions_xy == -1).all(dim=-1, keepdim=True)  # (..., L, 1)
    kernel_ordered_positions = kernel_ordered_positions * (~padding).float() + positions_xy.float() * padding.float()

    # Reshape positions and take min within each kernel to get the merged position
    kernel_ordered_positions = kernel_ordered_positions.reshape(*batch_shape, length, k * k, 2)
    new_positions = torch.div(kernel_ordered_positions, k, rounding_mode="floor")
    # For each merged patch, take the minimum position across the kernel
    new_positions = new_positions.min(dim=-2)[0].to(torch.long)

    return merged_patches, new_positions


def patches_merge(
    patches: "torch.Tensor",
    positions_xy: "torch.Tensor",
    length: int,
) -> tuple["torch.Tensor", "torch.Tensor"]:
    """Merge k×k groups of small patches into larger patches.

    Given `L` input patches of dimension `D = patch_size² × 3`, merge groups of
    `k×k` spatially adjacent patches into `length` output patches of dimension
    `(k × patch_size)² × 3`. The spatial grouping is determined by integer-dividing
    the XY positions by `k`.

    Args:
        patches: (*, L, D) — input patches.
        positions_xy: (*, L, 2) — integer XY positions for each patch (-1 for padding).
        length: target number of output patches. Must satisfy L = length × k².

    Returns:
        merged_patches: (*, length, k²×D) — merged patch features.
        merged_positions: (*, length, 2) — new XY positions for merged patches.
    """
    patch_size = math.isqrt(patches.shape[-1] // 3)
    if patches.shape[-1] != patch_size * patch_size * 3:
        raise ValueError(f"Patch dimension {patches.shape[-1]} is not a valid `patch_size * patch_size * 3`")

    k = math.isqrt(patches.shape[-2] // length)
    if k * k * length != patches.shape[-2]:
        raise ValueError(f"Cannot merge {patches.shape} to {length}")

    # Compute target ordering for reordering patches into kernel-grouped order.
    # This ensures patches within each k×k kernel are contiguous.
    max_x = positions_xy[..., 0].max(dim=-1, keepdim=True)[0] + 1
    kernel_idxs = torch.div(positions_xy, k, rounding_mode="floor")
    num_patches_from_top_left = k * k * kernel_idxs[..., 0] + k * max_x * kernel_idxs[..., 1]

    position_within_kernel = torch.remainder(positions_xy, k)
    num_patches_from_top_left_of_kernel = position_within_kernel[..., 0] + position_within_kernel[..., 1] * k
    target_ordering = num_patches_from_top_left_of_kernel + num_patches_from_top_left

    # Reorder patches by computing the inverse permutation via argsort,
    # then gathering patches into kernel-grouped order.
    perm = target_ordering.long().argsort(dim=-1)  # inverse permutation
    # Expand perm indices to match patch feature dimension for gathering
    perm_expanded = perm.unsqueeze(-1).expand_as(patches)
    kernel_ordered_patches = patches.gather(-2, perm_expanded)

    batch_shape = patches.shape[:-2]

    # Reshape: (*, length*k*k, patch_size*patch_size*3) → (*, length, (k*patch_size)*(k*patch_size)*3)
    kernel_ordered_patches = kernel_ordered_patches.reshape(*batch_shape, length, k * k, patch_size, patch_size, 3)
    # Rearrange (l, a*b, p, q, c) → (l, a*p, b*q, c)
    kernel_ordered_patches = kernel_ordered_patches.reshape(*batch_shape, length, k, k, patch_size, patch_size, 3)
    kernel_ordered_patches = kernel_ordered_patches.permute(
        *range(len(batch_shape)), -6, -5, -3, -4, -2, -1
    )  # (..., l, k, p, k, q, c)
    merged_patches = kernel_ordered_patches.reshape(*batch_shape, length, k * patch_size * k * patch_size * 3)

    # Compute new positions for merged patches
    perm_pos = perm.unsqueeze(-1).expand_as(positions_xy)
    kernel_ordered_positions = positions_xy.float().gather(-2, perm_pos.long())

    # Handle padding: preserve -1 positions
    padding = (positions_xy == -1).all(dim=-1, keepdim=True)  # (..., L, 1)
    kernel_ordered_positions = kernel_ordered_positions * (~padding).float() + positions_xy.float() * padding.float()

    # Reshape positions and take min within each kernel to get the merged position
    kernel_ordered_positions = kernel_ordered_positions.reshape(*batch_shape, length, k * k, 2)
    new_positions = torch.div(kernel_ordered_positions, k, rounding_mode="floor")
    # For each merged patch, take the minimum position across the kernel
    new_positions = new_positions.min(dim=-2)[0].to(torch.long)

    return merged_patches, new_positions

