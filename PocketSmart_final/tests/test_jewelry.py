def test_jewelry_text_only(client, registered_user):
    r=client.post('/api/generate-jewelry',headers={'Authorization':'Bearer '+registered_user['token']},data={'budget':'25000','occasion':'Wedding','style':'Elegant','city':'Mumbai','metal':'Any','outfit_notes':'Blue dress'})
    assert r.status_code == 200
    assert r.json()['planner']=='jewelry'

def test_jewelry_rejects_bad_image(client, registered_user):
    r=client.post('/api/generate-jewelry',headers={'Authorization':'Bearer '+registered_user['token']},data={'budget':'25000','occasion':'Wedding'},files={'outfit':('x.txt',b'hello','text/plain')})
    assert r.status_code == 415
