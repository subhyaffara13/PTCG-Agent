
def _check_group_features(info, parsed):
    """Checks whether the reverse and fuzzy features of the group calls match
    the groups which they call.
    """
    call_refs = {}
    additional_groups = []
    for call, reverse, fuzzy in info.group_calls:
        # Look up the reference of this group call.
        key = (call.group, reverse, fuzzy)
        ref = call_refs.get(key)
        if ref is None:
            # This group doesn't have a reference yet, so look up its features.
            if call.group == 0:
                # Calling the pattern as a whole.
                rev = bool(info.flags & REVERSE)
                fuz = isinstance(parsed, Fuzzy)
                if (rev, fuz) != (reverse, fuzzy):
                    # The pattern as a whole doesn't have the features we want,
                    # so we'll need to make a copy of it with the desired
                    # features.
                    additional_groups.append((CallRef(len(call_refs), parsed),
                      reverse, fuzzy))
            else:
                # Calling a capture group.
                def_info = info.defined_groups[call.group]
                group = def_info[0]
                if def_info[1 : ] != (reverse, fuzzy):
                    # The group doesn't have the features we want, so we'll
                    # need to make a copy of it with the desired features.
                    additional_groups.append((group, reverse, fuzzy))

            ref = len(call_refs)
            call_refs[key] = ref

        call.call_ref = ref

    info.call_refs = call_refs
    info.additional_groups = additional_groups

