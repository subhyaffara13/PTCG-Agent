
def _getAxisLabelsForUserLocation(
    axes: list[Union[AxisDescriptor, DiscreteAxisDescriptor]],
    userLocation: SimpleLocationDict,
) -> list[AxisLabelDescriptor]:
    labels: list[AxisLabelDescriptor] = []

    allAxisLabels = _getSortedAxisLabels(axes)
    if allAxisLabels.keys() != userLocation.keys():
        LOGGER.warning(
            f"Mismatch between user location '{userLocation.keys()}' and available "
            f"labels for '{allAxisLabels.keys()}'."
        )

    for axisName, axisLabels in allAxisLabels.items():
        userValue = userLocation[axisName]
        label: Optional[AxisLabelDescriptor] = next(
            (
                l
                for l in axisLabels
                if l.userValue == userValue
                or (
                    l.userMinimum is not None
                    and l.userMaximum is not None
                    and l.userMinimum <= userValue <= l.userMaximum
                )
            ),
            None,
        )
        if label is None:
            LOGGER.debug(
                f"Document needs a label for axis '{axisName}', user value '{userValue}'."
            )
        else:
            labels.append(label)

    return labels

