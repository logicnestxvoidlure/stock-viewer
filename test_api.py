import json
from app import app

def test_endpoints():
    client = app.test_client()
    
    print("Testing /api/search?q=apple ...")
    res = client.get("/api/search?q=apple")
    print(f"Status: {res.status_code}, Results: {len(res.json)}")
    assert res.status_code == 200
    
    print("\nTesting /api/quote?symbol=AAPL ...")
    res = client.get("/api/quote?symbol=AAPL")
    print(f"Status: {res.status_code}, Data: {json.dumps(res.json, indent=2)}")
    assert res.status_code == 200
    assert "price" in res.json
    
    print("\nTesting /api/history?symbol=AAPL&range=1mo ...")
    res = client.get("/api/history?symbol=AAPL&range=1mo")
    print(f"Status: {res.status_code}, Candles count: {len(res.json.get('candles', []))}")
    assert res.status_code == 200
    assert len(res.json.get("candles", [])) > 0
    
    print("\nTesting /api/market-summary ...")
    res = client.get("/api/market-summary")
    print(f"Status: {res.status_code}, Indices count: {len(res.json.get('indices', []))}, Popular count: {len(res.json.get('popular', []))}")
    assert res.status_code == 200

    print("\nTesting /api/news?symbol=AAPL ...")
    res = client.get("/api/news?symbol=AAPL")
    print(f"Status: {res.status_code}, News items: {len(res.json)}")
    assert res.status_code == 200
    
    print("\nTesting root / ...")
    res = client.get("/")
    print(f"Status: {res.status_code}, Content length: {len(res.data)}")
    assert res.status_code == 200

    print("\n>>> ALL TESTS PASSED SUCCESSFULLY! <<<")

if __name__ == "__main__":
    test_endpoints()
