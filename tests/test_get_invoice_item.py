from lib.error import errorcodes


def test__with_invalid_invoice_id(client):
    # act
    response = client.get("/invoices/123/items/456")
    # assert
    assert response.status_code == 404
    assert response.json['error']['code'] == errorcodes.resource_not_found.code
    assert response.json['error']['message'] == errorcodes.resource_not_found.message


def test__with_invalid_invoice_item_id(client):
    # arrange
    post_invoice_response = client.post('/invoices',
                                        json={
                                            'date': '2012-02-23'
                                        })
    invoice_id = post_invoice_response.json['id']
    # act
    response = client.get(f"/invoices/{invoice_id}/items/456")
    # assert
    assert response.status_code == 404
    assert response.json['error']['code'] == errorcodes.resource_not_found.code
    assert response.json['error']['message'] == errorcodes.resource_not_found.message
