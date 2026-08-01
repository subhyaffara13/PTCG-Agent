
def stuff(request, monkeypatch, distutils_managed_tempdir):
    self = request.instance
    tmp_dir = self.mkdtemp()
    self.root_target = os.path.join(tmp_dir, 'deep')
    self.target = os.path.join(self.root_target, 'here')
    self.target2 = os.path.join(tmp_dir, 'deep2')


def stuff(request, tmp_path):
    self = request.instance
    self.source = tmp_path / 'f1'
    self.target = tmp_path / 'f2'
    self.target_dir = tmp_path / 'd1'


def stuff(request, monkeypatch, distutils_managed_tempdir):
    self = request.instance
    self.python_h = os.path.join(self.mkdtemp(), 'python.h')
    monkeypatch.setattr(sysconfig, 'get_config_h_filename', self._get_config_h_filename)
    monkeypatch.setattr(sys, 'version', sys.version)

