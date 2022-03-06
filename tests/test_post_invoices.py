from lib.error import errorcodes


def test__with_empty_body(client):
    # act
    response = client.post('/invoices',
                           json={})
    # assert
    assert response.status_code == 400
    assert response.json['error']['code'] == errorcodes.invalid_request.code
    assert response.json['error']['message'] == errorcodes.invalid_request.message
    reasons = response.json['error']['reasons']
    required_fields = ['date']
    assert len(reasons) == len(required_fields)
    for index, reason in enumerate(reasons):
        field_name = required_fields[index]
        assert reason['code'] == errorcodes.missing_field.code
        assert reason['message'] == f"Missing field '{field_name}'"
        assert reason['path'] == [field_name]


def test__with_wrong_date_format(client):
    # arrange
    value = '231312-02-23'
    # act
    response = client.post('/invoices',
                           json={
                               'date': value
                           })
    # assert
    assert response.status_code == 400
    assert response.json['error']['code'] == errorcodes.invalid_request.code
    assert response.json['error']['message'] == errorcodes.invalid_request.message
    reasons = response.json['error']['reasons']
    assert len(reasons) == 1
    reason = reasons[0]
    field_name = 'date'
    assert reason['code'] == errorcodes.invalid_value.code
    assert reason['message'] == f"'{value}' is not a valid value for date format YYYY-MM-DD"
    assert reason['path'] == [field_name]


def test__with_wrong_date_value(client):
    # arrange
    value = '2012-22-23'
    # act
    response = client.post('/invoices',
                           json={
                               'date': value
                           })
    # assert
    assert response.status_code == 400
    assert response.json['error']['code'] == errorcodes.invalid_request.code
    assert response.json['error']['message'] == errorcodes.invalid_request.message
    reasons = response.json['error']['reasons']
    assert len(reasons) == 1
    reason = reasons[0]
    field_name = 'date'
    assert reason['code'] == errorcodes.invalid_value.code
    assert reason['message'] == f"'{value}' is not a valid value for date format YYYY-MM-DD"
    assert reason['path'] == [field_name]


def test__with_valid_payload(client):
    # arrange
    date = '2012-02-23'
    # act
    response = client.post('/invoices',
                           json={
                               'date': date
                           })
    # assert
    assert response.status_code == 200
    assert response.json['date'] == date
    invoice_id = response.json['id']

    get_response = client.get(f'/invoices/{invoice_id}')
    assert get_response.json['id'] == invoice_id
    assert get_response.json['date'] == date
