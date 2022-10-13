import json

from requests.auth import _basic_auth_str

from .conftest import client

# Data to test

mimetype = 'application/json'
headers = {
        'Content-Type': mimetype,
        'Accept': mimetype
    }
correct_params = {
        'rows': '10',
        'q': 'moon',
        'exact': 'False'
    }
incorrect_params = {
        'rows': '10',
        'q': 'moon',
        'exact': 'False',
        'other': 'test'
    }
correct_params_random = {
        'q': 'moon',
    }


test_suggestion = {
            "author": "Flaubert",
            "quote": "Une citation",
            "source": "unknonwn"
}

incomplete_suggestion = {
            "author": "",
            "quote": "",
            "source": ""
}

test_update = {
        "quote_id": "5",
        "author": "Victor Hugo",
        "quote": "Je passe le test",
        "source": "Les Misérables",
        "category": "unknown"
    }

bad_update = {
        "quote_id":"",
        "author": "",
        "source": "",
        "category": ""
    }


def test_api_base(client):
    response = client.get('/api/')
    assert response.status_code == 200


def test_api_search(client):
    response = client.get('/api/search')
    assert response.status_code == 200
    response = client.get('/api/search?rows=10&q=moon&exact=true')
    assert response.status_code == 200
    # post with no params, returns all quotes by default
    response = client.post('/api/search')
    assert response.status_code == 200
    # post with paramas
    response = client.post('/api/search', data=json.dumps(correct_params), headers=headers)
    assert response.status_code == 200
    # post with bad params
    response = client.post('/api/search', data=json.dumps(incorrect_params), headers=headers)
    assert response.status_code == 400


def test_api_random(client):
    response = client.get('/api/random')
    assert response.status_code == 200
    response = client.get('/api/random?q=moon')
    assert response.status_code == 200
    response = client.post('/api/random', data=json.dumps(correct_params_random), headers=headers)
    assert response.status_code == 200
    # post with bad params
    response = client.post('/api/random', data=json.dumps(incorrect_params), headers=headers)
    assert response.status_code == 400


def test_series(client):
    response = client.get('/api/authors')
    assert response.status_code == 200
    assert len(response.data.decode()) != 0
    response = client.get('/api/categories')
    assert response.status_code == 200
    assert len(response.data.decode()) != 0
    response = client.get('/api/sources')
    assert response.status_code == 200
    assert len(response.data.decode()) != 0


def test_suggest(client):
    response = client.post('/api/suggest_quote', data=json.dumps(test_suggestion), headers=headers)
    assert response.status_code == 200
    response = client.post('/api/suggest_quote', data=json.dumps(incomplete_suggestion), headers=headers)
    assert response.status_code == 400


def test_with_auth(client):
    credentials = {
        'username': 'test-admin',
        'password': 'test-admin'
    }
    # delete quote
    response = client.delete('/api/delete_quote/1')
    assert response.status_code == 401
    response = client.delete('/api/delete_quote/1', headers={
        'Authorization': _basic_auth_str(credentials['username'], credentials['password'])
    })
    assert response.status_code == 200
    response = client.delete('/api/delete_quote/1', headers={
        'Authorization': _basic_auth_str(credentials['username'], credentials['password'])
    })
    assert response.status_code == 400
    # update quote
    response = client.put('/api/update_quote', data=json.dumps(test_update), headers={
        'Authorization': _basic_auth_str(credentials['username'], credentials['password']),
        'Content-Type': mimetype,
        'Accept': mimetype
    })
    assert response.status_code == 200
    response = client.put('/api/update_quote', data=json.dumps(bad_update), headers={
        'Authorization': _basic_auth_str(credentials['username'], credentials['password']),
        'Content-Type': mimetype,
        'Accept': mimetype
    })
    assert response.status_code == 400
