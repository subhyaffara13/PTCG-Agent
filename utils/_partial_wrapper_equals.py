
def _partial_wrapper_equals(obs_or_fq1: _PartialWrapper, obs_or_fq2: _PartialWrapper):
    """
    Return whether the two partial wrappers are equal,
    """
    # functools.partial has no __eq__ operator defined so '==' defaults to 'is'
    obs_or_fq1_keywords = copy.copy(obs_or_fq1.p.keywords)
    obs_or_fq2_keywords = copy.copy(obs_or_fq2.p.keywords)
    keywords_equal = True
    # compare observer constructor with _obs_or_fq_ctr_equals since direct compare would fail
    if "observer" in obs_or_fq1_keywords and "observer" in obs_or_fq2_keywords:
        keywords_equal = keywords_equal and _obs_or_fq_ctr_equals(
            obs_or_fq1_keywords["observer"], obs_or_fq2_keywords["observer"]
        )
        obs_or_fq1_keywords.pop("observer")
        obs_or_fq2_keywords.pop("observer")
    keywords_equal = keywords_equal and obs_or_fq1_keywords == obs_or_fq2_keywords
    return (
        obs_or_fq1.p.func == obs_or_fq2.p.func
        and obs_or_fq1.p.args == obs_or_fq2.p.args
        and keywords_equal
    )

