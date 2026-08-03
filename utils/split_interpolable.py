import itertools
from typing import Tuple

def splitInterpolable(
    doc: DesignSpaceDocument,
    makeNames: bool = True,
    expandLocations: bool = True,
    makeInstanceFilename: MakeInstanceFilenameCallable = defaultMakeInstanceFilename,
) -> Iterator[Tuple[SimpleLocationDict, DesignSpaceDocument]]:
    """Split the given DS5 into several interpolable sub-designspaces.
    There are as many interpolable sub-spaces as there are combinations of
    discrete axis values.

    E.g. with axes:
        - italic (discrete) Upright or Italic
        - style (discrete) Sans or Serif
        - weight (continuous) 100 to 900

    There are 4 sub-spaces in which the Weight axis should interpolate:
    (Upright, Sans), (Upright, Serif), (Italic, Sans) and (Italic, Serif).

    The sub-designspaces still include the full axis definitions and STAT data,
    but the rules, sources, variable fonts, instances are trimmed down to only
    keep what falls within the interpolable sub-space.

    Args:
      - ``makeNames``: Whether to compute the instance family and style
        names using the STAT data.
      - ``expandLocations``: Whether to turn all locations into "full"
        locations, including implicit default axis values where missing.
      - ``makeInstanceFilename``: Callable to synthesize an instance filename
        when makeNames=True, for instances that don't specify an instance name
        in the designspace. This part of the name generation can be overridden
        because it's not specified by the STAT table.

    .. versionadded:: 5.0
    """
    discreteAxes = []
    interpolableUserRegion: Region = {}
    for axis in doc.axes:
        if hasattr(axis, "values"):
            # Mypy doesn't support narrowing union types via hasattr()
            # TODO(Python 3.10): use TypeGuard
            # https://mypy.readthedocs.io/en/stable/type_narrowing.html
            axis = cast(DiscreteAxisDescriptor, axis)
            discreteAxes.append(axis)
        else:
            axis = cast(AxisDescriptor, axis)
            interpolableUserRegion[axis.name] = Range(
                axis.minimum,
                axis.maximum,
                axis.default,
            )
    valueCombinations = itertools.product(*[axis.values for axis in discreteAxes])
    for values in valueCombinations:
        discreteUserLocation = {
            discreteAxis.name: value
            for discreteAxis, value in zip(discreteAxes, values)
        }
        subDoc = _extractSubSpace(
            doc,
            {**interpolableUserRegion, **discreteUserLocation},
            keepVFs=True,
            makeNames=makeNames,
            expandLocations=expandLocations,
            makeInstanceFilename=makeInstanceFilename,
        )
        yield discreteUserLocation, subDoc

