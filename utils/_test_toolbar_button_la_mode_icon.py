import os

def _test_toolbar_button_la_mode_icon(fig):
    # test a toolbar button icon using an image in LA mode (GH issue 25174)
    # create an icon in LA mode
    with tempfile.TemporaryDirectory() as tempdir:
        img = Image.new("LA", (26, 26))
        tmp_img_path = os.path.join(tempdir, "test_la_icon.png")
        img.save(tmp_img_path)

        class CustomTool(ToolToggleBase):
            image = tmp_img_path
            description = ""  # gtk3 backend does not allow None

        toolmanager = fig.canvas.manager.toolmanager
        toolbar = fig.canvas.manager.toolbar
        toolmanager.add_tool("test", CustomTool)
        toolbar.add_tool("test", "group")

