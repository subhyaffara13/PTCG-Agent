import re

def _un_chain(path, kwargs):
    # Avoid a circular import
    from fsspec.implementations.chained import ChainedFileSystem

    if "::" in path:
        x = re.compile(".*[^a-z]+.*")  # test for non protocol-like single word
        known_protocols = set(available_protocols())
        bits = []

        # split on '::', then ensure each bit has a protocol
        for p in path.split("::"):
            if p in known_protocols:
                bits.append(p + "://")
            elif "://" in p or x.match(p):
                bits.append(p)
            else:
                bits.append(p + "://")
    else:
        bits = [path]

    # [[url, protocol, kwargs], ...]
    out = []
    previous_bit = None
    kwargs = kwargs.copy()

    for bit in reversed(bits):
        protocol = kwargs.pop("protocol", None) or split_protocol(bit)[0] or "file"
        cls = get_filesystem_class(protocol)
        extra_kwargs = cls._get_kwargs_from_urls(bit)
        kws = kwargs.pop(protocol, {})

        if bit is bits[0]:
            kws.update(kwargs)

        kw = dict(
            **{k: v for k, v in extra_kwargs.items() if k not in kws or v != kws[k]},
            **kws,
        )
        bit = cls._strip_protocol(bit)

        if (
            "target_protocol" not in kw
            and issubclass(cls, ChainedFileSystem)
            and not bit
        ):
            # replace bit if we are chaining and no path given
            bit = previous_bit

        out.append((bit, protocol, kw))
        previous_bit = bit

    out.reverse()
    return out

