import os

def test_autolev_tutorial():

    dir_path = os.path.join(FILE_DIR, 'autolev', 'test-examples',
                            'autolev-tutorial')

    if os.path.isdir(dir_path):
        l = ["tutor1", "tutor2", "tutor3", "tutor4", "tutor5", "tutor6",
             "tutor7"]
        for i in l:
            in_filepath = os.path.join("autolev-tutorial", i + ".al")
            out_filepath = os.path.join("autolev-tutorial", i + ".py")
            _test_examples(in_filepath, out_filepath, i)

