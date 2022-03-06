from lib.error import errorcodes


def test__with_invalid_invoice_id(client):
    # act
    response = client.get("/invoices/123")
    # assert
    assert response.status_code == 404
    assert response.json['error']['code'] == errorcodes.resource_not_found.code
    assert response.json['error']['message'] == errorcodes.resource_not_found.message
