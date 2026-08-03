from typing import Any, Dict, List

def _subsetRulesBasedOnConditions(
    rules: List[RuleDescriptor], designRegion: Region
) -> List[RuleDescriptor]:
    # What rules to keep:
    #  - Keep the rule if any conditionset is relevant.
    #  - A conditionset is relevant if all conditions are relevant or it is empty.
    #  - A condition is relevant if
    #    - axis is point (C-AP),
    #       - and point in condition's range (C-AP-in)
    #            (in this case remove the condition because it's always true)
    #       - else (C-AP-out) whole conditionset can be discarded (condition false
    #         => conditionset false)
    #    - axis is range (C-AR),
    #       - (C-AR-all) and axis range fully contained in condition range: we can
    #         scrap the condition because it's always true
    #       - (C-AR-inter) and intersection(axis range, condition range) not empty:
    #         keep the condition with the smaller range (= intersection)
    #       - (C-AR-none) else, whole conditionset can be discarded
    newRules: List[RuleDescriptor] = []
    for rule in rules:
        newRule: RuleDescriptor = RuleDescriptor(
            name=rule.name, conditionSets=[], subs=rule.subs
        )
        for conditionset in rule.conditionSets:
            cs = _conditionSetFrom(conditionset)
            newConditionset: List[Dict[str, Any]] = []
            discardConditionset = False
            for selectionName, selectionValue in designRegion.items():
                # TODO: Ensure that all(key in conditionset for key in region.keys())?
                if selectionName not in cs:
                    # raise Exception("Selection has different axes than the rules")
                    continue
                if isinstance(selectionValue, (float, int)):  # is point
                    # Case C-AP-in
                    if selectionValue in cs[selectionName]:
                        pass  # always matches, conditionset can stay empty for this one.
                    # Case C-AP-out
                    else:
                        discardConditionset = True
                else:  # is range
                    # Case C-AR-all
                    if selectionValue in cs[selectionName]:
                        pass  # always matches, conditionset can stay empty for this one.
                    else:
                        intersection = cs[selectionName].intersection(selectionValue)
                        # Case C-AR-inter
                        if intersection is not None:
                            newConditionset.append(
                                {
                                    "name": selectionName,
                                    "minimum": intersection.minimum,
                                    "maximum": intersection.maximum,
                                }
                            )
                        # Case C-AR-none
                        else:
                            discardConditionset = True
            if not discardConditionset:
                newRule.conditionSets.append(newConditionset)
        if newRule.conditionSets:
            newRules.append(newRule)

    return newRules

