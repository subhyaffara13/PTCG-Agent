import os

def test_save_unicode_field(tmpdir):
    filename = os.path.join(str(tmpdir), 'test.mat')
    test_dict = {'a':{'b':1,'c':'test_str'}}
    savemat(filename, test_dict)

