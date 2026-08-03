from typing import Tuple

def _getRibbiStyle(
    self: DesignSpaceDocument, userLocation: SimpleLocationDict
) -> Tuple[RibbiStyleName, SimpleLocationDict]:
    """Compute the RIBBI style name of the given user location,
    return the location of the matching Regular in the RIBBI group.

    .. versionadded:: 5.0
    """
    regularUserLocation = {}
    axes_by_tag = {axis.tag: axis for axis in self.axes}

    bold: bool = False
    italic: bool = False

    axis = axes_by_tag.get("wght")
    if axis is not None:
        for regular_label in axis.axisLabels:
            if (
                regular_label.linkedUserValue == userLocation[axis.name]
                # In the "recursive" case where both the Regular has
                # linkedUserValue pointing the Bold, and the Bold has
                # linkedUserValue pointing to the Regular, only consider the
                # first case: Regular (e.g. 400) has linkedUserValue pointing to
                # Bold (e.g. 700, higher than Regular)
                and regular_label.userValue < regular_label.linkedUserValue
            ):
                regularUserLocation[axis.name] = regular_label.userValue
                bold = True
                break

    axis = axes_by_tag.get("ital") or axes_by_tag.get("slnt")
    if axis is not None:
        for upright_label in axis.axisLabels:
            if (
                upright_label.linkedUserValue == userLocation[axis.name]
                # In the "recursive" case where both the Upright has
                # linkedUserValue pointing the Italic, and the Italic has
                # linkedUserValue pointing to the Upright, only consider the
                # first case: Upright (e.g. ital=0, slant=0) has
                # linkedUserValue pointing to Italic (e.g ital=1, slant=-12 or
                # slant=12 for backwards italics, in any case higher than
                # Upright in absolute value, hence the abs() below.
                and abs(upright_label.userValue) < abs(upright_label.linkedUserValue)
            ):
                regularUserLocation[axis.name] = upright_label.userValue
                italic = True
                break

    return BOLD_ITALIC_TO_RIBBI_STYLE[bold, italic], {
        **userLocation,
        **regularUserLocation,
    }

