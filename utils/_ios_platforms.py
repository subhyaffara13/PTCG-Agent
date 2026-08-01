
def _ios_platforms(arch: str) -> list[str]:
    match = _apple_arch_pat.match(arch)
    if match:
        name, major, minor, actual_multiarch = match.groups()
        ios_version = (int(major), int(minor))
        arches = [
            # Since we have always only checked that the platform starts
            # with "ios", for backwards-compatibility we extract the
            # actual prefix provided by the user in case they provided
            # something like "ioscustom_". It may be good to remove
            # this as undocumented or deprecate it in the future.
            "{}_{}".format(name, arch[len("ios_") :])
            for arch in ios_platforms(ios_version, actual_multiarch)
        ]
    else:
        # arch pattern didn't match (?!)
        arches = [arch]
    return arches

