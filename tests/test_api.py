def test_evaluate_flag_success(client):

    response = client.post(
        "/api/v1/flags/evaluate",
        headers={"X-Tenant-ID": "tenant_123"},
        json={"flag_key": "new_landing_page"},
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["flag_key"] == "new_landing_page"
    assert data["is_enabled"] is True
    assert data["reason"] == "MATCHED_STATIC_RULE"


def test_evaluate_flag_failure(client):

    response = client.post(
        "/api/v1/flags/evaluate",
        headers={
            "X-Tenant-ID": "tenant_123",
        },
        json={"flag_key": "ab"},
    )

    assert response.status_code == 422
    data = response.get_json()
    assert "errors" in data
    assert "flag_key" in data["errors"]


def test_evaluate_flag_not_found_fallback(client):

    response = client.post(
        "/api/v1/flags/evaluate",
        headers={"X-Tenant-ID": "tenant_123"},
        json={"flag_key": "non_existent"},
    )

    assert response.status_code == 200
    data = response.get_json()
    assert data["is_enabled"] is False
    assert data["reason"] == "FLAG NOT FOUND DEFAULT OFF"
