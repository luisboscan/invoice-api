from assertpy import assert_that


def test__with_no_invoices(client):
    # act
    response = client.get("/invoices")
    # assert
    assert response.status_code == 200
    assert response.json == []


def test__with_invoices(client):
    # arrange
    client.post('/invoices',
                json={
                    'date': '2012-02-23'
                })
    client.post('/invoices',
                json={
                    'date': '2021-11-04'
                })
    # act
    response = client.get("/invoices")
    # assert
    assert response.status_code == 200
    assert len(response.json) == 2
    assert_that(response.json[0]).contains('id')
    assert response.json[0]['date'] == '2012-02-23'
    assert response.json[1]['date'] == '2021-11-04'
