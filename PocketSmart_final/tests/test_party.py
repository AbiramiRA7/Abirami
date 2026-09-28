def test_party_fallback(client, registered_user):
    r=client.post('/api/generate-party',headers={'Authorization':'Bearer '+registered_user['token']},json={'budget':100000,'guests':50,'event_type':'Birthday','venue':'Hall','city':'Mumbai','preferences':''})
    assert r.status_code == 200
    data=r.json()
    assert data['planner']=='party'
    assert len(data['recommendations'])==5
