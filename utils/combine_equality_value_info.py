
def combine_equality_value_info(infos: Iterable[EqualityValueInfo]) -> EqualityValueInfo:
    domains: dict[str, EqualityDomainInfo] = {}
    is_top = False
    for info in infos:
        for domain, domain_info in info.domains.items():
            existing_domain_info = domains.get(domain)
            if existing_domain_info is None:
                domains[domain] = EqualityDomainInfo(
                    set(domain_info.type_names), set(domain_info.enum_type_names)
                )
            else:
                existing_domain_info.type_names.update(domain_info.type_names)
                existing_domain_info.enum_type_names.update(domain_info.enum_type_names)
        is_top = is_top or info.is_top
    return EqualityValueInfo(domains, is_top)

