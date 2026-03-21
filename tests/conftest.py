import pytest


class _FakeResponse:
    """Stub for requests.post() responses in unit tests."""

    def __init__(self, payload, status_code=200):
        self._payload = payload
        self.status_code = status_code
        self.text = str(payload)

    def json(self):
        return self._payload


@pytest.fixture
def fake_headers():
    return {
        "Authorization": "Bearer test-token",
        "Content-Type": "application/json",
    }
