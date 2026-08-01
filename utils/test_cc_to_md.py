
def test_cc_to_md():
    md = tools.dict_to_md({'filename': CC_TO_MD_RESULTS})
    _md = '''
| Filename | Name | Type | Start:End Line | Complexity | Classification |
| -------- | ---- | ---- | -------------- | ---------- | -------------- |
| filename | Classname.flush | M | 110:117 | 2 | A |
| filename | Classname | C | 73:124 | 4 | B |
| filename | decrement | F | 62:69 | 10 | C |
'''
    assert md == _md

