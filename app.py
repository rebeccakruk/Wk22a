from flask import Flask, make_response, jsonify, request
from dbcreds import production_mode
from dbhelpers import run_statement

app = Flask(__name__)

@app.get('/api/candy')
def get_all_candy():
    candies = []
    keys = ["id", "name", "owner"]
    result = run_statement("CALL get_all_candy()")
    if (type(result) == list):
        for candy in result:
            candies.append(dict(zip(keys, candy)))
            # candies.append(candy[0])
            # candies.append(candy[1])
        return make_response(jsonify(candies), 200)
    else:
        return make_response(jsonify(result), 500)
    
@app.get('/api/users')
def get_id():
    username = request.args.get('username')
    password = request.args.get('password')
    result = run_statement("CALL id(?,?)", [username, password])
    if (type(result) == list):
        for user in result:
            user_id = user[0]
            login(user_id)
        return user_id
    else: 
        return make_response(jsonify(result), 500)
@app.post('/api/users')
def login(user_id:int):
    result = run_statement("CALL user_login(?)", [user_id])
    if result == None:
        get_token(user_id)
        return "You have successfully logged in!"
    else:
        return "Something went wrong, please try again"

@app.get('/api/users/token')
def get_token(user_id:int):
    sesh = []
    result = run_statement("CALL get_token(?)", [user_id])
    if result != None:
        token = result[0]
        for token in result:
            sesh.append(token[1])
        return token

# @app.post('/api/candy')
# def add_candy():
#     candy = request.json.get('name')
#     user_Id = request.json.get('user_Id')
#     result = run_statement("CALL new_candy(?, ?)", [candy, user_Id])
#     if result == None:
#         return "You've successfully added {} to the list!".format(candy)
#     else: 
#         return "Something went wrong, please try again."

@app.post('/api/candy_new')
def add_new():
    candy = request.json.get('name')
    result = run_statement("CALL add_new(?)", [candy])
    if result == None:
        return "You've successfully added {} to the list!".format(candy)
    else: 
        return "Something went wrong, please try again."


@app.delete('/api/candy')
def clear_candy():
    candy_id = request.json.get('id')
    candies = []
    keys = ["id", "name"]
    if (candy_id == None):
        return "Please enter a valid candy name"
    result = run_statement("CALL clear_candy(?)", [candy_id])
    if result != None:
        for candy in candies:
            candies.append(dict(zip(keys, candy)))
        return "You have successfully deleted {} from the list.".format(candy_id)
    else:
        return "Unable to delete {} from the list.".format(candy_id)
    
@app.patch('/api/candy_change')
def change_candy():
    candy_id = request.json.get('id')
    candy = request.json.get('name')
    if (candy == None):
        return "Please enter a valid candy name"
    result = run_statement("CALL change_candy(?, ?)", [candy_id, candy])
    if result == None:
        return "You have successfully changed the candy name to {}".format(candy)
    else:
        return "Something went wrong, please try again."    

if (production_mode == True):
    print("Running server in production mode")
    import bjoern #type:ignore
    bjoern.run(app, "0.0.0.0", 5000)
else:
    print("Running in testing mode")
    from flask_cors import CORS
    CORS(app)
    app.run(debug=True)