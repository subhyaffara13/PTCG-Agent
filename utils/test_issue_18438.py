
def test_issue_18438():
    assert pickle.loads(pickle.dumps(S.Half)) == S.Half

