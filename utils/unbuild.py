import sys

def unbuild(font, f=sys.stdout):
    fvar = font["fvar"]
    axes = fvar.axes
    segments, mappings = mappings_from_avar(font)

    if "name" in font:
        name = font["name"]
        axisNames = {
            axis.axisTag: name.getDebugName(axis.axisNameID) or axis.axisTag
            for axis in axes
        }
    else:
        axisNames = {a.axisTag: a.axisTag for a in axes}

    print("<?xml version='1.0' encoding='UTF-8'?>", file=f)
    print('<designspace format="5.1">', file=f)
    print("  <axes>", file=f)
    for axis in axes:

        axisName = axisNames[axis.axisTag]

        triplet = (axis.minValue, axis.defaultValue, axis.maxValue)
        triplet = [int(v) if v == int(v) else v for v in triplet]

        axisMap = segments.get(axis.axisTag)
        closing = "/>" if axisMap is None else ">"

        print(
            f'    <axis tag="{axis.axisTag}" name="{axisName}" minimum="{triplet[0]}" maximum="{triplet[2]}" default="{triplet[1]}"{closing}',
            file=f,
        )
        if axisMap is not None:
            for k in sorted(axisMap.keys()):
                v = axisMap[k]
                k = int(k) if k == int(k) else k
                v = int(v) if v == int(v) else v
                print(f'      <map input="{k}" output="{v}"/>', file=f)
            print("    </axis>", file=f)
    if mappings:
        print("    <mappings>", file=f)
        for inputLoc, outputLoc in mappings:
            print("      <mapping>", file=f)
            print("        <input>", file=f)
            for tag in sorted(inputLoc.keys()):
                v = inputLoc[tag]
                v = int(v) if v == int(v) else v
                print(
                    f'          <dimension name="{axisNames[tag]}" xvalue="{v}"/>',
                    file=f,
                )
            print("        </input>", file=f)
            print("        <output>", file=f)
            for tag in sorted(outputLoc.keys()):
                v = outputLoc[tag]
                v = int(v) if v == int(v) else v
                print(
                    f'          <dimension name="{axisNames[tag]}" xvalue="{v}"/>',
                    file=f,
                )
            print("        </output>", file=f)
            print("      </mapping>", file=f)
        print("    </mappings>", file=f)
    print("  </axes>", file=f)
    print("</designspace>", file=f)

