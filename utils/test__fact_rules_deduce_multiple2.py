
def test_FactRules_deduce_multiple2():
    f = FactRules(['real == neg | zero | pos'])

    def D(facts):
        kb = FactKB(f)
        kb.deduce_all_facts(facts)
        return kb

    assert D({'real': T}) == {'real': T}
    assert D({'real': F}) == {'real': F, 'neg': F, 'zero': F, 'pos': F}
    assert D({'neg': T}) == {'real': T, 'neg': T}
    assert D({'zero': T}) == {'real': T, 'zero': T}
    assert D({'pos': T}) == {'real': T, 'pos': T}

    # --- key tests below ---
    assert D({'neg': F, 'zero': F, 'pos': F}) == {'real': F, 'neg': F,
             'zero': F, 'pos': F}
    assert D({'real': T, 'neg': F}) == {'real': T, 'neg': F}
    assert D({'real': T, 'zero': F}) == {'real': T, 'zero': F}
    assert D({'real': T, 'pos': F}) == {'real': T, 'pos': F}

    assert D({'real': T,           'zero': F, 'pos': F}) == {'real': T,
             'neg': T, 'zero': F, 'pos': F}
    assert D({'real': T, 'neg': F,            'pos': F}) == {'real': T,
             'neg': F, 'zero': T, 'pos': F}
    assert D({'real': T, 'neg': F, 'zero': F          }) == {'real': T,
             'neg': F, 'zero': F, 'pos': T}

    assert D({'neg': T, 'zero': F, 'pos': F}) == {'real': T, 'neg': T,
             'zero': F, 'pos': F}
    assert D({'neg': F, 'zero': T, 'pos': F}) == {'real': T, 'neg': F,
             'zero': T, 'pos': F}
    assert D({'neg': F, 'zero': F, 'pos': T}) == {'real': T, 'neg': F,
             'zero': F, 'pos': T}

