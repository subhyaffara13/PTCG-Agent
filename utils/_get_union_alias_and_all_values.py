from typing import Any, Tuple

def _get_union_alias_and_all_values(
    union_type: Type[Any], discriminator_key: str
) -> Tuple[str, Tuple[Tuple[str, ...], ...]]:
    zipped_aliases_values = [get_discriminator_alias_and_values(t, discriminator_key) for t in get_args(union_type)]
    # unzip: [('alias_a',('v1', 'v2)), ('alias_b', ('v3',))] => [('alias_a', 'alias_b'), (('v1', 'v2'), ('v3',))]
    all_aliases, all_values = zip(*zipped_aliases_values)
    return get_unique_discriminator_alias(all_aliases, discriminator_key), all_values

