<span id="top"></span>
# Quote Generator REST API services 
## [prefix endpoint: /api]

Version: 1.0.0

Author: Lucas Terriel

License: MIT

## Summary

- <a href="#default">Default</a>
    - <a href="#end_b">/</a>
- <a href="#quotes">Quotes</a>
  - <a href="#end_s">search/</a>
  - <a href="#end_r">random/</a>
- <a href="#quotes_store">Quotes store</a>
  - <a href="#end_a">authors/</a>
  - <a href="#end_c">categories/</a>
  - <a href="#end_sources">sources/</a>
- <a href="#quotes_users">Quotes users</a>
  - <a href="#end_sq">suggest_quote/</a>
  - <a href="#end_rq">remove_quote/</a>
  - <a href="#end_uq">update_quote/</a>

## Response status codes 

| HTTP Status code | Signification                                                               |
|------------------|-----------------------------------------------------------------------------|
| 200              | Successful operation.                                                       |
| 400              | Wrong request, missing parameters, missing header                           |
| 404              | ressource not found                                                         |
| 405              | Method not allowed                                                          |
| 500              | Indicate an internal service error, further described by a provided message |



## <p id="default">Default</p>

*Quote generator default endpoints*

---

### <p id="end_b">/</p> 

- **Description**: Retrieve generic information about Quote Generator API service

| Method	 | Request type 	                    | Response type 		    |
|---------|-----------------------------------|---------------------|
| GET	    | application/x-www-form-urlencoded | application/json  	 | 


- **Parameters**

None

- **Testing** (use client like [Postman](https://www.postman.com/) or **cURL** command line)

> ```bash
$ curl http://127.0.0.1:3000/api/ 
```

The successful operation will return:

> ```bash
{
    "info": {
     "name": "Quote Generator API",
     "version": "1.0",
     "status": True,
    }
}
```

## <p id="quotes">Quotes</p>

*Quote generator endpoints to play with quotes*

---

### <p id="end_s">/search</p>

- **Description**: Find and filter quotes or a specific quote from Quote generator API with defined parameters. By default,
returns all quotes from database.

| Method	 | Request type 	                    | Response type 		    |
|---------|-----------------------------------|---------------------|
| GET	    | application/x-www-form-urlencoded | application/json  	 | 
| POST	   | application/json | application/json  	 |


- **Request headers**:

| required	                                                                       | name 	       | value 		            | description                          |
|---------------------------------------------------------------------------------|--------------|---------------------|--------------------------------------|
| required (POST, if query is provided else returns all quotes) / optional (GET)	 | Accept       | application/json  	 | Set the response type of the output  |
| required (POST, if query is provided else returns all quotes) / optional (GET)	 | Content-type | application/json  	 | Set the parameters type of the input |



- **Parameters**

| required	 | name       | content-type value 		 | description                                                    |
|-----------|------------|-----------------------|----------------------------------------------------------------|
| optional	      | rows       | Integer 	             | Limit the number of results in response                        |
| optional	     | q          | String 	              | Keyword or any string to be retrieved in all quotes            |
| optional	     | exact      | Boolean  	            | Set true to exact match, else fuzzy match (Defaults to: false) |


- **Testing** 

> ```bash
$ curl -X POST http://127.0.0.1:3000/api/search -d '{"rows": 100, "q": "moon", "exact": true}' -H 'accept: application/json' -H 'content-type: application/json'
```



The successful operation will return:

> ```bash
{
    "info": {
        "name": "Quote Generator API",
        "version": "1.0",
        "status": true
    },
    "parameters": {
        "rows": 100,
        "q": "moon",
        "exact": true
    },
    "results": {
        "TotalQuotes": 45,
        "quotes": [
            {
                "quote_id": 1848,
                "quote": "Life is too short to not have fun; we are only here for a short time compared to the sun and the moon and all that.",
                "author": "Coolio",
                "source": "unknown",
                "category": "life"
            },
            {
                "quote_id": 3439,
                "quote": "Don't tell me the moon is shining; show me the glint of light on broken glass.",
                "author": "Anton Chekhov",
                "source": "unknown",
                "category": "writing"
            },
            ...
```


### <p id="end_r">/random</p> 

- **Description**: Returns a random quote or a random quote that contains a term from a user.

| Method	 | Request type 	                    | Response type 		    |
|---------|-----------------------------------|---------------------|
| GET	    | application/x-www-form-urlencoded | application/json  	 | 
| POST	   | application/json | application/json  	 |


- **Request headers**:

| required	                                                                           | name 	       | value 		            | description                          |
|-------------------------------------------------------------------------------------|--------------|---------------------|--------------------------------------|
| required (POST, if query is provided else returns a random quote) / optional (GET)	 | Accept       | application/json  	 | Set the response type of the output  |
| required (POST, if query is provided else returns a random quote) / optional (GET)	                             | Content-type | application/json  	 | Set the parameters type of the input |


- **Parameters**

| required	 | name       | content-type value 		 | description                                                            |
|-----------|------------|-----------------------|------------------------------------------------------------------------|
| optional	     | q          | String 	              | Keyword or any string to be retrieved a random that contains this term |

- **Testing** 

> ```bash
$ curl -X POST http://127.0.0.1:3000/api/random -d '{"q": "moon"}' -H 'accept: application/json' -H 'content-type: application/json'
```



The successful operation will return:

> ```bash
{
    "info": {
        "name": "Quote Generator API",
        "version": "1.0",
        "status": true
    },
    "parameters": {
        "q": "moon"
    },
    "results": {
        "quote_id": 27062,
        "quote": "Let the love of the moon kiss you good night, let the morning sun wake you up with loving light.",
        "author": "Debasish Mridha",
        "source": "unknown",
        "category": "philosophy"
    }
}
```

## <p id="quotes_store">Quotes store</p>

*Quote generator endpoints to access to specific data from database*

---

### <p id="end_a">/authors</p> 

- **Description**: Retrieve all authors list from Quote Generator API service

| Method	 | Request type 	                    | Response type 		    |
|---------|-----------------------------------|---------------------|
| GET	    | application/x-www-form-urlencoded | application/json  	 | 


- **Parameters**

None

- **Testing**

> ```bash
$ curl http://127.0.0.1:3000/api/authors 
```

The successful operation will return:

> ```bash
{
    "info": {
        "name": "Quote Generator API",
        "version": "1.0",
        "status": true
    },
    "results": {
        "authors": [
            "Dr. Seuss",
            "Marilyn Monroe",
            "Oscar Wilde",
            "Albert Einstein",
            "William W. Purkey",
            "Marcus Tullius Cicero",
            ...
                    ]
    }
}
```

### <p id="end_c">/categories</p>


- **Description**: Retrieve all categories list from Quote Generator API service

| Method	 | Request type 	                    | Response type 		    |
|---------|-----------------------------------|---------------------|
| GET	    | application/x-www-form-urlencoded | application/json  	 | 


- **Parameters**

None

- **Testing**

> ```bash
$ curl http://127.0.0.1:3000/api/categories 
```

The successful operation will return:

> ```bash
{
    "info": {
        "name": "Quote Generator API",
        "version": "1.0",
        "status": true
    },
    "results": {
        "categories": [
            "life",
            "love",
            "inspiration",
            "humor",
            "soul",
            "truth",
            "poetry",
            "wisdom",
            "friendship",
            "happiness",
            ...
                    ]
    }
}
```


### <p id="end_sources">/sources</p>

- **Description**: Retrieve all sources list from Quote Generator API service

| Method	 | Request type 	                    | Response type 		    |
|---------|-----------------------------------|---------------------|
| GET	    | application/x-www-form-urlencoded | application/json  	 | 


- **Parameters**

None

- **Testing**

> ```bash
$ curl http://127.0.0.1:3000/api/sources 
```

The successful operation will return:

> ```bash
{
    "info": {
        "name": "Quote Generator API",
        "version": "1.0",
        "status": true
    },
    "results": {
        "sources": [
            "unknown",
            "This is My Story",
            "A Testament of Hope: The Essential Writings and Speeches",
            "Twilight of the Idols",
            "The Perks of Being a Wallflower",
            "The Fellowship of the Ring",
            ...
                    ]
    }
}
```

## <p id="quotes_users">Quotes users</p>

*Quote generator endpoints to add, update or remove a quote from database*

---

### <p id="end_sq">/suggest_quote</p>


- **Description**: Suggest a new quote entry.

| Method	 | Request type 	                    | Response type 		    |
|---------|-----------------------------------|---------------------|
| POST	   | application/json | application/json  	 |


- **Request headers**:

| required	                                                                       | name 	       | value 		            | description                          |
|---------------------------------------------------------------------------------|--------------|---------------------|--------------------------------------|
| required 	 | Accept       | application/json  	 | Set the response type of the output  |
| required 	 | Content-type | application/json  	 | Set the parameters type of the input |



- **Parameters**

| required	 | name   | content-type value 		 | description                                                        |
|-----------|--------|-----------------------|--------------------------------------------------------------------|
| required	 | author | String 		             | Author of the quote submitted                                      |
| required	 | quote  | String 	              | Text of the quote submitted                                        |
| optional	 | source | String 	  	            | Source (Books, Album etc.) where the quote submitted was extracted |


- **Testing** 

> ```bash
curl -X POST http://127.0.0.1:3000/api/suggest_quote -H 'accept: application/json' -H 'content-type: application/json' -d '{"author": "Flaubert", "quote": "a citation", "source": "unknonwn"}'
```

The successful operation will return:

> ```bash
{
    "type": "Your quote is submitted, our team check this new quote before add it to database",
    "quote_submitted": {
        "author": "Flaubert",
        "quote": "a citation",
        "source": "unknonwn"
    }
}
```

### <p id="end_rq">/remove\_quote/<id_quote> (Basic authentification required)</p>

- **Description**: Delete a quote entry in database according to its ID.

| Method	 | Request type 	                    | Response type 		    |
|---------|-----------------------------------|---------------------|
| GET	    | application/x-www-form-urlencoded | application/json  	 |
| DELETE	 | application/x-www-form-urlencoded | application/json  	 |

- **Request headers**:

| required	                                                                       | name 	       | value 		            | description                          |
|---------------------------------------------------------------------------------|--------------|---------------------|--------------------------------------|
| required 	 | Accept       | application/json  	 | Set the response type of the output  |
| required 	 | Content-type | application/json  	 | Set the parameters type of the input |



- **Parameters**

| required	 | name     | content-type value 		 | description                    |
|-----------|----------|-----------------------|--------------------------------|
| required	 | quote_id | Integer 		            | Unique ID of quote in database |


- **Testing** 

> ```bash
curl -X DELETE \
  http://127.0.0.1:3000/api/delete_quote/5 \
  -H 'accept: application/json' \
  -H 'authorization: Basic dGVzdC1hZG1pbjp0ZXN0LWFkbWlu' \
  -H 'content-type: application/json'
```

The successful operation will return:

> ```bash
{
    "info": {
        "name": "Quote Generator API",
        "version": "1.0",
        "status": true
    },
    "parameters": {
        "quote_id": 5
    },
    "results": {
        "quote_delete": {
            "quote_id": 5,
            "quote": "You've gotta dance like there's nobody watching,Love like you'll never be hurt,Sing like there's nobody listening,And live like it's heaven on earth.",
            "author": "William W. Purkey",
            "source": "unknown",
            "category": "love"
        }
    }
}
```


### <p id="end_uq">/update\_quote (Basic authentification required)</p>

- **Description**: Update a quote entry in database according to its ID.

| Method	 | Request type 	                    | Response type 		    |
|---------|-----------------------------------|---------------------|
| PUT	    | application/json | application/json  	 |
| POST	   | application/json | application/json  	 |

- **Request headers**:

| required	                                                                       | name 	       | value 		            | description                          |
|---------------------------------------------------------------------------------|--------------|---------------------|--------------------------------------|
| required 	 | Accept       | application/json  	 | Set the response type of the output  |
| required 	 | Content-type | application/json  	 | Set the parameters type of the input |



- **Parameters**

| required	 | name     | content-type value 		 | description                                                        |
|-----------|----------|-----------------------|--------------------------------------------------------------------|
| required	 | quote_id | Integer 		            | Unique ID of quote in database                                     |
| optional	 | author   | String 		             | Author of the quote submitted                                      |
| optional	 | quote    | String 	              | Text of the quote submitted                                        |
| optional	 | source   | String 	  	            | Source (Books, Album etc.) where the quote submitted was extracted |
| optional	 | category | String 	  	            | Category of quote                                                  |


- **Testing** 

> ```bash
curl -X POST \
  http://127.0.0.1:3000/api/update_quote \
  -H 'accept: application/json' \
  -H 'authorization: Basic dGVzdC1hZG1pbjp0ZXN0LWFkbWlu' \
  -H 'content-type: application/json' \
  -d '{
        "quote_id": "7",
        "author": "Victor Hugo",
        "quote": "Une citation mise à jour",
        "source": "Les Misérables",
        "category": "unknown"
    }'
```

The successful operation will return:

> ```bash
{
    "info": {
        "name": "Quote Generator API",
        "version": "1.0",
        "status": true
    },
    "parameters": {
        "quote_id": "7",
        "author": "Victor Hugo",
        "quote": "Une citation mise à jour",
        "source": "Les Misérables",
        "category": "unknown"
    },
    "results": {
        "quote_updated": {
            "quote_id": 7,
            "quote": "",
            "author": "Victor Hugo",
            "source": "Les Misérables",
            "category": "unknown"
        }
    }
}
```

<a href="#top">Go to the top</a>