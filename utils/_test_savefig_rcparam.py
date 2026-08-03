import os
from pathlib import Path


def _test_savefig_rcparam():
    tmp_path = Path(os.environ["TEST_SAVEFIG_PATH"])

    def new_choose_save_file(title, directory, filename):
        # Replacement function instead of opening a GUI window
        # Make a new directory for testing the update of the rcParams
        assert directory == str(tmp_path)
        os.makedirs(f"{directory}/test")
        return f"{directory}/test/{filename}"

    fig = plt.figure()
    with (mock.patch("matplotlib.backends._macosx.choose_save_file",
                     new_choose_save_file),
          mpl.rc_context({"savefig.directory": tmp_path})):
        fig.canvas.toolbar.save_figure()
        # Check the saved location got created
        save_file = f"{tmp_path}/test/{fig.canvas.get_default_filename()}"
        assert os.path.exists(save_file)

        # Check the savefig.directory rcParam got updated because
        # we added a subdirectory "test"
        assert mpl.rcParams["savefig.directory"] == f"{tmp_path}/test"

