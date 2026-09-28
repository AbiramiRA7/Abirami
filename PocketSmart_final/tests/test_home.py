def test_home_requires_auth(client):
    r=client.post('/api/generate-home',json={'budget':50000,'rooms':['Living Room'],'items':[{'name':'Lights','quantity':2}]})
    assert r.status_code == 401

def test_home_fallback(client, registered_user):
    r=client.post('/api/generate-home',headers={'Authorization':'Bearer '+registered_user['token']},json={'budget':50000,'rooms':['Living Room'],'items':[{'name':'Lights','quantity':2}],'style':'modern','city':'Mumbai'})
    assert r.status_code == 200
    assert r.json()['source']=='fallback'
    assert len(r.json()['recommendations']) >= 1
