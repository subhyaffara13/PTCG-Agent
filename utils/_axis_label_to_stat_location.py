from typing import Dict

def _axisLabelToStatLocation(
    label: AxisLabelDescriptor,
) -> Dict:
    label_format = label.getFormat()
    name = {"en": label.name, **label.labelNames}
    flags = _labelToFlags(label)
    if label_format == 1:
        return dict(name=name, value=label.userValue, flags=flags)
    if label_format == 3:
        return dict(
            name=name,
            value=label.userValue,
            linkedValue=label.linkedUserValue,
            flags=flags,
        )
    if label_format == 2:
        res = dict(
            name=name,
            nominalValue=label.userValue,
            flags=flags,
        )
        if label.userMinimum is not None:
            res["rangeMinValue"] = label.userMinimum
        if label.userMaximum is not None:
            res["rangeMaxValue"] = label.userMaximum
        return res
    raise NotImplementedError("Unknown STAT label format")

