from lib.error import errorcodes


def test__with_empty_body(client):
    # arrange
    post_invoice_response = client.post('/invoices',
                                        json={
                                            'date': '2012-02-23'
                                        })
    invoice_id = post_invoice_response.json['id']
    # act
    response = client.post(f'/invoices/{invoice_id}/items',
                           json={})
    # assert
    assert response.status_code == 400
    assert response.json['error']['code'] == errorcodes.invalid_request.code
    assert response.json['error']['message'] == errorcodes.invalid_request.message
    reasons = response.json['error']['reasons']
    required_fields = ['units', 'description', 'amount']
    assert len(reasons) == len(required_fields)
    for index, reason in enumerate(reasons):
        field_name = required_fields[index]
        assert reason['code'] == errorcodes.missing_field.code
        assert reason['message'] == f"Missing field '{field_name}'"
        assert reason['path'] == [field_name]


def test__with_lower_than_min_amount(client):
    # arrange
    post_invoice_response = client.post('/invoices',
                                        json={
                                            'date': '2012-02-23'
                                        })
    invoice_id = post_invoice_response.json['id']
    # act
    response = client.post(f'/invoices/{invoice_id}/items',
                           json={
                               'units': 2,
                               'description': 'Team event dinner',
                               'amount': -4.5
                           })
    # assert
    assert response.status_code == 400
    assert response.json['error']['code'] == errorcodes.invalid_request.code
    assert response.json['error']['message'] == errorcodes.invalid_request.message
    reasons = response.json['error']['reasons']
    assert len(reasons) == 1
    reason = reasons[0]
    field_name = 'amount'
    assert reason['code'] == errorcodes.invalid_value.code
    assert reason['message'] == f"Invalid value for field '{field_name}', value cannot be lower than: 0"
    assert reason['path'] == [field_name]


def test__with_bigger_than_max_amount(client):
    # arrange
    post_invoice_response = client.post('/invoices',
                                        json={
                                            'date': '2012-02-23'
                                        })
    invoice_id = post_invoice_response.json['id']
    # act
    response = client.post(f'/invoices/{invoice_id}/items',
                           json={
                               'units': 2,
                               'description': 'Team event dinner',
                               'amount': 1000000
                           })
    # assert
    assert response.status_code == 400
    assert response.json['error']['code'] == errorcodes.invalid_request.code
    assert response.json['error']['message'] == errorcodes.invalid_request.message
    reasons = response.json['error']['reasons']
    assert len(reasons) == 1
    reason = reasons[0]
    field_name = 'amount'
    assert reason['code'] == errorcodes.invalid_value.code
    assert reason['message'] == f"Invalid value for field '{field_name}', value cannot be higher than: 999999.99"
    assert reason['path'] == [field_name]


def test__with_lower_than_min_units(client):
    # arrange
    post_invoice_response = client.post('/invoices',
                                        json={
                                            'date': '2012-02-23'
                                        })
    invoice_id = post_invoice_response.json['id']
    # act
    response = client.post(f'/invoices/{invoice_id}/items',
                           json={
                               'units': 0,
                               'description': 'Team event dinner',
                               'amount': 123.34
                           })
    # assert
    assert response.status_code == 400
    assert response.json['error']['code'] == errorcodes.invalid_request.code
    assert response.json['error']['message'] == errorcodes.invalid_request.message
    reasons = response.json['error']['reasons']
    assert len(reasons) == 1
    reason = reasons[0]
    field_name = 'units'
    assert reason['code'] == errorcodes.invalid_value.code
    assert reason['message'] == f"Invalid value for field '{field_name}', value cannot be lower than: 1"
    assert reason['path'] == [field_name]


def test__with_higher_than_max_units(client):
    # arrange
    post_invoice_response = client.post('/invoices',
                                        json={
                                            'date': '2012-02-23'
                                        })
    invoice_id = post_invoice_response.json['id']
    # act
    response = client.post(f'/invoices/{invoice_id}/items',
                           json={
                               'units': 100000,
                               'description': 'Team event dinner',
                               'amount': 123.34
                           })
    # assert
    assert response.status_code == 400
    assert response.json['error']['code'] == errorcodes.invalid_request.code
    assert response.json['error']['message'] == errorcodes.invalid_request.message
    reasons = response.json['error']['reasons']
    assert len(reasons) == 1
    reason = reasons[0]
    field_name = 'units'
    assert reason['code'] == errorcodes.invalid_value.code
    assert reason['message'] == f"Invalid value for field '{field_name}', value cannot be higher than: 99999"
    assert reason['path'] == [field_name]


def test__with_empty_description(client):
    # arrange
    post_invoice_response = client.post('/invoices',
                                        json={
                                            'date': '2012-02-23'
                                        })
    invoice_id = post_invoice_response.json['id']
    # act
    response = client.post(f'/invoices/{invoice_id}/items',
                           json={
                               'units': 3,
                               'description': '',
                               'amount': 123.34
                           })
    # assert
    assert response.status_code == 400
    assert response.json['error']['code'] == errorcodes.invalid_request.code
    assert response.json['error']['message'] == errorcodes.invalid_request.message
    reasons = response.json['error']['reasons']
    assert len(reasons) == 1
    reason = reasons[0]
    field_name = 'description'
    assert reason['code'] == errorcodes.empty_field.code
    assert reason['message'] == f"Empty field '{field_name}'"
    assert reason['path'] == [field_name]


def test__with_invalid_invoice_id(client):
    # act
    response = client.post("/invoices/123/items",
                           json={
                               'units': 2,
                               'description': 'Team event dinner',
                               'amount': 123.34
                           })
    # assert
    assert response.status_code == 404
    assert response.json['error']['code'] == errorcodes.resource_not_found.code
    assert response.json['error']['message'] == errorcodes.resource_not_found.message


def test__with_valid_payload(client):
    # arrange
    post_invoice_response = client.post('/invoices',
                                        json={
                                            'date': '2012-02-23'
                                        })
    invoice_id = post_invoice_response.json['id']
    units = 3
    description = 'Team event dinner'
    amount = 123.34
    # act
    response = client.post(f'/invoices/{invoice_id}/items',
                           json={
                               'units': units,
                               'description': description,
                               'amount': amount
                           })
    # assert
    assert response.status_code == 200
    assert response.json['units'] == units
    assert response.json['description'] == description
    assert response.json['amount'] == amount
    invoice_item_id = response.json['id']

    get_response = client.get(f'/invoices/{invoice_id}/items/{invoice_item_id}')
    assert get_response.json['id'] == invoice_item_id
    assert get_response.json['invoiceId'] == invoice_id
    assert get_response.json['units'] == units
    assert get_response.json['description'] == description
    assert get_response.json['amount'] == amount
