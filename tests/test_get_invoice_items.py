from assertpy import assert_that

from lib.error import errorcodes


def test__with_invalid_invoice_id(client):
    # act
    response = client.get("/invoices/123/items")
    # assert
    assert response.status_code == 404
    assert response.json['error']['code'] == errorcodes.resource_not_found.code
    assert response.json['error']['message'] == errorcodes.resource_not_found.message


def test__with_no_invoice_items(client):
    # arrange
    post_invoice_response = client.post('/invoices',
                                        json={
                                            'date': '2012-02-23'
                                        })
    invoice_id = post_invoice_response.json['id']
    # act
    response = client.get(f"/invoices/{invoice_id}/items")
    # assert
    assert response.status_code == 200
    assert response.json == []


def test__with_invoice_items(client):
    # arrange
    post_invoice_response = client.post('/invoices',
                                        json={
                                            'date': '2012-02-23'
                                        })
    invoice_id = post_invoice_response.json['id']
    client.post(f'/invoices/{invoice_id}/items',
                json={
                    'units': 2,
                    'description': 'Invoice 1',
                    'amount': 123.45
                })
    client.post(f'/invoices/{invoice_id}/items',
                json={
                    'units': 5,
                    'description': 'Invoice 2',
                    'amount': 678.91
                })
    # act
    response = client.get(f'/invoices/{invoice_id}/items')
    # assert
    assert response.status_code == 200
    assert len(response.json) == 2
    assert_that(response.json[0]).contains('id')
    assert response.json[0]['units'] == 2
    assert response.json[0]['description'] == 'Invoice 1'
    assert response.json[0]['amount'] == 123.45
    assert response.json[1]['units'] == 5
    assert response.json[1]['description'] == 'Invoice 2'
    assert response.json[1]['amount'] == 678.91
