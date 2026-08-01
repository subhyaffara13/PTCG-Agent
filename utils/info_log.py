
def info_log(request, monkeypatch):
    self = request.instance
    self._logs = []
    monkeypatch.setattr(log, 'info', self._info)

