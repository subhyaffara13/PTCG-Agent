
def remove_unused_subroutines(cff):
    for fontname in cff.keys():
        font = cff[fontname]
        cs = font.CharStrings
        # Renumber subroutines to remove unused ones

        # Mark all used subroutines
        for c in cs.values():
            subrs = getattr(c.private, "Subrs", [])
            decompiler = _MarkingT2Decompiler(subrs, c.globalSubrs, c.private)
            decompiler.execute(c)

        all_subrs = [font.GlobalSubrs]
        if hasattr(font, "FDArray"):
            all_subrs.extend(
                fd.Private.Subrs
                for fd in font.FDArray
                if hasattr(fd.Private, "Subrs") and fd.Private.Subrs
            )
        elif hasattr(font.Private, "Subrs") and font.Private.Subrs:
            all_subrs.append(font.Private.Subrs)

        subrs = set(subrs)  # Remove duplicates

        # Prepare
        for subrs in all_subrs:
            if not hasattr(subrs, "_used"):
                subrs._used = set()
            subrs._used = _uniq_sort(subrs._used)
            subrs._old_bias = calcSubrBias(subrs)
            subrs._new_bias = calcSubrBias(subrs._used)

        # Renumber glyph charstrings
        for c in cs.values():
            subrs = getattr(c.private, "Subrs", None)
            _cs_subset_subroutines(c, subrs, font.GlobalSubrs)

        # Renumber subroutines themselves
        for subrs in all_subrs:
            if subrs == font.GlobalSubrs:
                if not hasattr(font, "FDArray") and hasattr(font.Private, "Subrs"):
                    local_subrs = font.Private.Subrs
                elif (
                    hasattr(font, "FDArray")
                    and len(font.FDArray) == 1
                    and hasattr(font.FDArray[0].Private, "Subrs")
                ):
                    # Technically we shouldn't do this. But I've run into fonts that do it.
                    local_subrs = font.FDArray[0].Private.Subrs
                else:
                    local_subrs = None
            else:
                local_subrs = subrs

            subrs.items = [subrs.items[i] for i in subrs._used]
            if hasattr(subrs, "file"):
                del subrs.file
            if hasattr(subrs, "offsets"):
                del subrs.offsets

            for subr in subrs.items:
                _cs_subset_subroutines(subr, local_subrs, font.GlobalSubrs)

        # Delete local SubrsIndex if empty
        if hasattr(font, "FDArray"):
            for fd in font.FDArray:
                _pd_delete_empty_subrs(fd.Private)
        else:
            _pd_delete_empty_subrs(font.Private)

        # Cleanup
        for subrs in all_subrs:
            del subrs._used, subrs._old_bias, subrs._new_bias


def remove_unused_subroutines(self):
    self.cff.remove_unused_subroutines()

