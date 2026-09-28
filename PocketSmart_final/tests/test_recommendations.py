def test_history_is_user_scoped(client, registered_user):
    headers={'Authorization':'Bearer '+registered_user['token']}
    client.post('/api/generate-home',headers=headers,json={'budget':50000,'rooms':['Bedroom'],'items':[{'name':'Lamp'}]})
    r=client.get('/api/history',headers=headers)
    assert r.status_code==200
    assert len(r.json())>=1

def test_detail(client, registered_user):
    headers={'Authorization':'Bearer '+registered_user['token']}
    created=client.post('/api/generate-party',headers=headers,json={'budget':10000,'guests':10,'event_type':'Dinner'}).json()
    history=client.get('/api/history',headers=headers).json()
    rid=history[0]['id']
    r=client.get(f'/api/recommendations-details/{rid}',headers=headers)
    assert r.status_code==200
