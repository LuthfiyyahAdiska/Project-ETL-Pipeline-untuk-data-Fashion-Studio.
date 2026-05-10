import requests
from utils import extract


# =========================
# TEST 1: SUCCESS PATH
# =========================
def test_scrape_success(monkeypatch):
    class FakeResponse:
        def raise_for_status(self):
            pass

        @property
        def content(self):
            return b"""
            <div class="collection-card">
                <h3 class="product-title">Test</h3>
                <div class="price">$10</div>
                <p>Rating: 5</p>
                <p>Colors: 2</p>
                <p>Size: M</p>
                <p>Gender: Unisex</p>
            </div>
            """

    class FakeSession:
        def get(self, url):
            return FakeResponse()

    monkeypatch.setattr(extract.requests, "Session", lambda: FakeSession())

    result = extract.scrape_all()

    assert isinstance(result, list)
    assert len(result) > 0


# =========================
# TEST 2: FORCE REQUEST ERROR (COVER 16–18)
# =========================
def test_scrape_request_error(monkeypatch):
    class FakeSession:
        def get(self, url):
            raise Exception("forced error")

    monkeypatch.setattr(extract.requests, "Session", lambda: FakeSession())

    result = extract.scrape_all()

    # tetap list karena loop lanjut
    assert isinstance(result, list)


# =========================
# TEST 3: FORCE PARSE ERROR (COVER 45–46)
# =========================
def test_scrape_parse_error(monkeypatch):
    class FakeResponse:
        def raise_for_status(self):
            pass

        @property
        def content(self):
            # ini bikin BeautifulSoup tidak nemu elemen → trigger except card
            return b"""
            <div class="collection-card">
                <h3 class="product-title"></h3>
                <!-- price hilang total biar .text strip error -->
            </div>
            """

    class FakeSession:
        def get(self, url):
            return FakeResponse()

    monkeypatch.setattr(extract.requests, "Session", lambda: FakeSession())

    result = extract.scrape_all()

    assert isinstance(result, list)