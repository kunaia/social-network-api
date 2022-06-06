# social-network-api
Rest API based social network

## used technologies
* Flask
* Flask_Restful
* Flask_jwt_extanded
* Flask_Marshmallow
* Flask_SQLAlchemy
* Flask_Migrate
* requests
* unittest
* 
* Postgresql
____
this api uses apstractapi.com as third party api to validate emails, get geolocation of ip-s and for checking holiday infos. So you need to register and get write corresponding API keys in .env file.

## How to Make Social Network API work?
1. setup conda environment with _conda_env.yml_ file and activate it
   * `conda env create -f conda_env.yml`
   * `conda activate social-network-api`
2. create _.env_ file in main directory and fill the fields shown in _.env.example_ file
3. run **Unittests** on api
   * `python -m unittest`
4. run api
   * `python app.py`

____
## API endpoints
* ### user resources
  * `[POST] /register` -- **user registration**. you need to pass following arguments:
    * name
    * surname
    * email
    * password
  * `[POST] /login` -- **user login**. arguments:
    * email
    * password
  * `[POST] /logout` -- **user logout**. on this call you just need to pass Authorization access_token that will be blocklisted
  * `[POST] /logout2` -- **user logout2**. on this call you just need to pass Authorization _refresh_token_ that will be blocklisted
  * `[GET] /user` -- **user info**. this endpoint gives you info of user with _access_token_. you just need to pass the Authorization token


* ### post resources
  * `[POST] /post` -- **post creating**. Authorization header is required. arguments:
    * body
  * `[GET] /posts` -- **get all posts**. Authorization header is optional.
  * `[GET/PUT/DELETE] /post/'int:post_id'` -- **post modification**. 
    1. Authorization header is optional for GET method, while it is required id PUT/DELETE methods
    2. in PUT method you have to pass argument:
       * body
  * `[POST] /post/'int:post_id'/like` -- **post Like/Unlike**. This endpoint toggles 'like' attribute on user_post connection. you just neet to pass Authorization header while requesting on this endpoint.
