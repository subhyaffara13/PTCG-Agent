
def _rand_eager_offsets_impl(offsets, device: torch.device) -> Tensor:
    """
    Batched version of _rand_eager_offset_impl. For each entry in `offsets`,
    reserve that many 32-bit Philox samples and return a 1D int64 tensor
    containing the packed (seed, base) values for each reservation.
    """
    states = [_reserve_rng_state(device, int(off)) for off in offsets]
    seeds = [s for s, _ in states]
    bases = [b for _, b in states]

    def _to_i64(x):
        if isinstance(x, torch.Tensor):
            return x
        return torch.as_tensor(x, device=device, dtype=torch.int64)

    seeds_tensor = torch.stack([_to_i64(x) for x in seeds]).view(-1)
    bases_tensor = torch.stack([_to_i64(x) for x in bases]).view(-1)
    packed = torch.stack([seeds_tensor, bases_tensor], dim=1)
    return packed

