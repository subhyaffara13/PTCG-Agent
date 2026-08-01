
def test_rule_tests():

    l = ["ruletest1", "ruletest2", "ruletest3", "ruletest4", "ruletest5",
         "ruletest6", "ruletest7", "ruletest8", "ruletest9", "ruletest10",
         "ruletest11", "ruletest12"]

    for i in l:
        in_filepath = i + ".al"
        out_filepath = i + ".py"
        _test_examples(in_filepath, out_filepath, i)

