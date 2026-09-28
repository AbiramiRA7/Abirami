def test_session_info(client, registered_user):
    r=client.get('/api/session-info',headers={'Authorization':'Bearer '+registered_user['token']})
    assert r.status_code==200
    assert r.json()['logged_in'] is True

def test_session_requires_auth(client):
    assert client.get('/api/session-info').status_code==401
