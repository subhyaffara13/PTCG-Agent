
def _fill_limit_area_2d(
    mask: npt.NDArray[np.bool_], limit_area: Literal["outside", "inside"]
) -> None:
    """Prepare 2d mask for ffill/bfill with limit_area.

    When called, mask will no longer faithfully represent when
    the corresponding are NA or not.

    Parameters
    ----------
    mask : np.ndarray[bool, ndim=1]
        Mask representing NA values when filling.
    limit_area : { "outside", "inside" }
        Whether to limit filling to outside or inside the outer most non-NA value.
    """
    neg_mask = ~mask.T
    if limit_area == "outside":
        # Identify inside
        la_mask = (
            np.maximum.accumulate(neg_mask, axis=0)
            & np.maximum.accumulate(neg_mask[::-1], axis=0)[::-1]
        )
    else:
        # Identify outside
        la_mask = (
            ~np.maximum.accumulate(neg_mask, axis=0)
            | ~np.maximum.accumulate(neg_mask[::-1], axis=0)[::-1]
        )
    mask[la_mask.T] = False

