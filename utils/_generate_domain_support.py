
def _generate_domain_support(dist_family):
    n_parameterizations = len(dist_family._parameterizations)

    domain = f"\nfor :math:`x \\in {dist_family._variable.domain}`.\n"

    if n_parameterizations == 0:
        support = """
        This class accepts no distribution parameters.
        """
    elif n_parameterizations == 1:
        support = f"""
        This class accepts one parameterization:
        {str(dist_family._parameterizations[0])}.
        """
    else:
        number = {2: 'two', 3: 'three', 4: 'four', 5: 'five'}[
            n_parameterizations]
        parameterizations = [f"- {str(p)}" for p in
                             dist_family._parameterizations]
        parameterizations = "\n".join(parameterizations)
        support = f"""
        This class accepts {number} parameterizations:

        {parameterizations}
        """
    support = "\n".join([line.lstrip() for line in support.split("\n")][1:])
    return domain + support

