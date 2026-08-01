
def isin_sorting(elements, test_elements, *, assume_unique=False, invert=False):
    elements_flat = elements.flatten()
    test_elements_flat = test_elements.flatten()
    if assume_unique:
        # This is the same as the aten implementation. For
        # assume_unique=False, we cannot use unique() here, so we use a
        # version with searchsorted instead.
        all_elements = torch.cat([elements_flat, test_elements_flat])
        sorted_elements, sorted_order = torch.sort(all_elements, stable=True)

        duplicate_mask = sorted_elements[1:] == sorted_elements[:-1]
        duplicate_mask = torch.constant_pad_nd(duplicate_mask, [0, 1], False)

        if invert:
            duplicate_mask = duplicate_mask.logical_not()

        mask = torch.empty_like(duplicate_mask)
        mask = mask.index_copy(0, sorted_order, duplicate_mask)

        return mask[0 : elements.numel()].reshape(elements.shape)
    else:
        sorted_test_elements, _ = torch.sort(test_elements_flat)
        idx = torch.searchsorted(sorted_test_elements, elements_flat)
        test_idx = torch.where(idx < sorted_test_elements.numel(), idx, 0)
        cmp = sorted_test_elements[test_idx] == elements_flat
        cmp = cmp.logical_not() if invert else cmp
        return cmp.reshape(elements.shape)

