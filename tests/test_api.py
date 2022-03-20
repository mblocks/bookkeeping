# -*- coding: utf-8 -*-


def test_query_bookkeepings(client):
    response = client.get("/")
    assert response.status_code == 200


def test_create_bookkeepings(client):
    payload = {
        "type": "income",
        "trade_at": "2020-01-01",
        "item": "test",
        "amount": "100",
        "owner": "test"
    }
    response = client.post("/", json=payload)
    assert response.status_code == 200
    assert response.json().get('month') == "2020-01"


def test_update_bookkeepings(client):
    payload = {
        "type": "income",
        "trade_at": "2020-01-01",
        "item": "test",
        "amount": "100",
        "owner": "test"
    }
    created_response = client.post("/", json=payload)
    created_bookkeeping = created_response.json()
    assert created_response.status_code == 200
    assert created_bookkeeping.get('month') == "2020-01"

    created_bookkeeping['amount'] = 420
    updated_response = client.post("/", json=created_bookkeeping)
    updated_bookkeeping = updated_response.json()
    assert updated_response.status_code == 200
    assert updated_bookkeeping.get('amount') == 420


def test_delete_bookkeepings(client):
    payload = {
        "type": "income",
        "trade_at": "2020-01-01",
        "item": "delete",
        "amount": "100",
        "owner": "test"
    }
    created_response = client.post("/", json=payload)
    created_bookkeeping = created_response.json()
    assert created_response.status_code == 200
    assert created_bookkeeping.get('month') == "2020-01"

    deleted_response = client.post(
        "/{}/delete".format(created_bookkeeping.get('id')))
    deleted_bookkeeping = deleted_response.json()
    assert deleted_response.status_code == 200
    assert deleted_bookkeeping.get('amount') == 100


def test_summary_bookkeepings(client):
    response = client.get("/summary")
    summary = response.json()
    assert response.status_code == 200
    assert 'total' in summary
    assert 'data' in summary
    assert 'trend' in summary


def test_export_bookkeepings(client):
    response = client.get("/export")
    assert response.status_code == 200


def test_import_bookkeepings(client):
    pass
