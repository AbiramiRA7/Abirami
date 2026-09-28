def test_register_and_login(client):
    r = client.post('/api/register', json={'name':'Alice','email':'alice@example.com','password':'password123'})
    assert r.status_code == 200
    assert r.json()['access_token']
    r = client.post('/api/login', json={'email':'alice@example.com','password':'password123'})
    assert r.status_code == 200

def test_duplicate_registration(client):
    payload={'name':'Bob','email':'bob@example.com','password':'password123'}
    assert client.post('/api/register',json=payload).status_code == 200
    assert client.post('/api/register',json=payload).status_code == 409
