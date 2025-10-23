import requests
from src.f1dash.utils.http import retry_get

class DummyResponse:
    def __init__(self, ok=True):
        self._ok = ok
        self.status_code = 200 if ok else 500
    def raise_for_status(self):
        if not self._ok:
            raise requests.HTTPError("bad response")

def test_retry_get_success(monkeypatch):
    monkeypatch.setattr("requests.get", lambda url, timeout, headers: DummyResponse(ok=True))
    r = retry_get("https://example.com")
    assert isinstance(r, DummyResponse)

def test_retry_get_fail(monkeypatch):
    def bad_get(*args, **kwargs): raise requests.ConnectionError("no net")
    monkeypatch.setattr("requests.get", bad_get)
    r = retry_get("https://example.com")
    assert r is None