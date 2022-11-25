import json
import pdb
from pymongo import MongoClient
from flask import Flask, request, jsonify, make_response
import bson.json_util as json_util

import requests
global_url = 'http://127.0.0.1:5000/'
# , Blueprint, Response
# from flask_cors import CORS

# from setup.configurations import *

app = Flask(__name__)
app.config["DEBUG"] = True

isTesting = True

def get_database(database_name):
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb+srv://tcc_avc:adm321@tcccluster.wzgcevd.mongodb.net/test"
    # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
    db_client = MongoClient(CONNECTION_STRING)
    # Create the database for our example (we will use the same database throughout the tutorial
    return db_client[database_name]

@app.route('/', methods=['GET'])
def home():
    return "this is an endpoint"



@app.route('/profile/<user_name>', methods=['GET'])
def get_user_profile(user_name):
    profile_collection = db_users['profile']
    message = profile_collection.find_one({"_user_name": user_name})

    # message received:
    # {'_id': ObjectId('6   329244d285409a800aa376e'), 'name': 'Joca Joao Joaquim', 'email': 'joca@email.com', 'investor': True, '_user_name': 'jocaJ'}

    if not message: return "FAILED TO GET PROFILE", 400
    return json.loads(json_util.dumps(message)), 200

@app.route('/profile', methods=['POST'])
def create_user_profile():
    data = request.get_json()

    if '_user_name' not in data: return "MISSING USER NAME", 400

    if not isTesting:
        # Certify all mandatory data will be set
        if 'password' not in data: return "MISSING PASSWORD", 400
        if 'investor' not in data: return "MISSING INVESTOR PROFILE", 400    
        if 'email' not in data: return "MISSING EMAIL", 400

    profile_collection = db_users['profile']
    message = profile_collection.insert_one(data)
    
    if not message.acknowledged: return "FAILED", 400    
    # we can also return message.inserted_id, but it does not seem to show good info
    users = get_user_profile(data['_user_name'])

    return users[0], 200


''' This endpoint DOES NOT REQUIRE receiving all data to be inserted, 
it can receive only the data that will be modified
also, check: https://www.mongodb.com/docs/manual/reference/operator/update/'''
@app.route('/profile/<user_name>', methods=['PUT'])
def update_user_profile(user_name):
    data = request.get_json()

    set_data = {
        "$set": data
    }

    profile_filter = {"_user_name" : user_name}
    profile_collection = db_users['profile']
    message = profile_collection.update_one(profile_filter, set_data)
    
    if not message.acknowledged:
        # raise Error
        return "FAILED", 400

    users = get_user_profile(data['_user_name'])
    return users[0], 200

@app.route('/profile/<user_name>', methods=['DELETE'])
def delete_user_profile(user_name):
    profile_to_remove = {"_user_name" : user_name}

    profile_collection = db_users['profile']
    message = profile_collection.delete_one(profile_to_remove)

    if not message.acknowledged or message.deleted_count != 1:
        # raise Error
        return "FAILED", 400
    return "USER DELETED", 200

@app.route('/company', methods=['POST'])
def create_company_raw_data():
    data = request.get_json()

    if '_company_cnpj' not in data: return "MISSING CNPJ", 400
    
    if not isTesting:
        # Certify all mandatory data will be set    
        if '_user_name' not in data: return "MISSING USER NAME", 400
        if 'oficial_name' not in data: return "MISSING OFICIAL NAME", 400    

    company_raw_data_collection = db_companies['raw_data']
    company_filter = { '$or': [
        {'_company_cnpj': data['_company_cnpj']},
        {'_company_id': data['_company_id']}
    ]}
    already_exists = company_raw_data_collection.find_one(company_filter)
    if already_exists:
        return "ALREADY INSERTED IN DATABASE", 400

    message = company_raw_data_collection.insert_one(data)    
    if not message.acknowledged:
        # raise Error
        return "FAILED", 400
    
    companies = get_company_raw_data(data['_company_id'])

    return companies[0], 200

@app.route('/company/<_company_id>', methods=['GET'])
def get_company_raw_data(_company_id):
    company_raw_data_collection = db_companies['raw_data']
    
    company_filter = {"_company_id" : int(_company_id)}
    message = company_raw_data_collection.find_one(company_filter)
    if not message:
        return "FAILED TO FIND COMPANY WHOSE ID IS "+_company_id, 400
    return json.loads(json_util.dumps(message)), 200

@app.route('/company/all', methods=['GET'])
def get_all_company_raw_data():
    company_raw_data_collection = db_companies['raw_data']
    
    message = company_raw_data_collection.find()
    if not message:
        return "NO DATA IN COLLECTION RAW DATA IN COMPANIES DB", 400
    return json.loads(json_util.dumps(message)), 200

@app.route('/company/<_company_id>', methods=['PUT'])
def update_company_raw_data(_company_id):
    data = request.get_json()
    company_raw_data_collection = db_companies['raw_data']

    company_filter = {"_company_id" : int(_company_id)}
    company_found = company_raw_data_collection.find_one(company_filter)
    if not company_found:
        return "FAILED TO FIND COMPANY WHOSE ID IS "+_company_id, 400
    
    message = company_raw_data_collection.update_one(company_filter, data)    

    if not message.acknowledged: return "FAILED TO UPDATE", 400
    return "COMPANY IDENTIFICATION UPDATED", 200

@app.route('/company/<_company_id>', methods=['DELETE'])
def delete_company_raw_data(_company_id):
    company_raw_data_collection = db_companies['raw_data']
    company_to_remove = {"_company_id" : int(_company_id)}

    company_found = company_raw_data_collection.find_one(company_to_remove)
    if not company_found:
        return "FAILED TO FIND COMPANY WHOSE ID IS "+_company_id, 400
    
    message = company_raw_data_collection.delete_one(company_to_remove)
    if not message.acknowledged or message.deleted_count != 1:
        return "FAILED TO DELETE COMPANY IDENTIFICATION", 400
    return "COMPANY IDENTIFICATION DELETED", 200

@app.route('/company_metrics/<_company_id>', methods=['POST'])
def create_company_metrics(_company_id):
    data = request.get_json()

    # Certify all mandatory data will be set    
    if '_company_id' not in data: return "MISSING COMPANY ID", 400
    if '_user_name' not in data: return "MISSING USER NAME", 400
    
    company_metrics_collection = db_companies['metrics']
    company_filter = { '$or': [
        {'_company_id': int(_company_id)}
    ]}
    already_exists = company_metrics_collection.find_one(company_filter)
    if already_exists:
        return "ALREADY INSERTED IN DATABASE", 400

    message = company_metrics_collection.insert_one(data)    
    if not message.acknowledged:
        # raise Error
        return "FAILED TO INSERT METRICS", 400
    return "COMPANY IDENTIFICATION ADDED SUCCESSFULLY", 200

@app.route('/company_metrics/<_company_id>', methods=['GET'])
def get_company_metrics(_company_id):
    company_metrics_collection = db_companies['metrics']
    
    company_filter = {"_company_id" : int(_company_id)}
    message = company_metrics_collection.find_one(company_filter)
    if not message:
        return "FAILED TO FIND COMPANY WHOSE ID IS "+_company_id, 400
    return json.loads(json_util.dumps(message)), 200
    
@app.route('/company_metrics/all', methods=['GET'])
def get_all_company_metrics():
    company_metrics_collection = db_companies['metrics']
    
    message = company_metrics_collection.find()
    if not message:
        return "NO DATA IN COLLECTION METRICS IN COMPANIES DB", 400
    return json.loads(json_util.dumps(message)), 200

@app.route('/company_metrics/<_company_id>', methods=['PUT'])
def update_company_metrics(_company_id):
    data = request.get_json()
    company_metrics_collection = db_companies['metrics']

    company_filter = {"_company_id" : int(_company_id)}
    company_found = company_metrics_collection.find_one(company_filter)
    if not company_found:
        return "FAILED TO FIND COMPANY WHOSE ID IS "+_company_id, 400
    
    message = company_metrics_collection.update_one(company_filter, data)    
    if not message.acknowledged: return "FAILED TO UPDATE", 400
    return "COMPANY IDENTIFICATION UPDATED", 200

@app.route('/company_metrics/<_company_id>', methods=['DELETE'])
def delete_company_metrics(_company_id):
    company_metrics_collection = db_companies['metrics']
    company_to_remove = {"_company_id" : int(_company_id)}

    company_found = company_metrics_collection.find_one(company_to_remove)
    if not company_found:
        return "FAILED TO FIND COMPANY WHOSE ID IS "+_company_id, 400
    
    message = company_metrics_collection.delete_one(company_to_remove)
    if not message.acknowledged or message.deleted_count != 1:
        return "FAILED TO DELETE COMPANY IDENTIFICATION", 400
    return "COMPANY IDENTIFICATION DELETED", 200

@app.route('/investors_theory', methods=['POST'])
def create_investors_theory():
    data = request.get_json()

    # Certify all mandatory data will be set    
    if '_user_name' not in data: return "MISSING USER NAME", 400
    
    profile_collection = db_users['profile']
    user_added = profile_collection.find_one({"_user_name": data['_user_name']})
    if not user_added:
        return "USER IS NOT IN DATABASE, PLEASE ADD USER FIRST"
    
    investors_theory_collection = db_investors['parameters_and_weights']

    most_recent_theory = investors_theory_collection.find_one(sort=[("_theory_id", -1)])
    if most_recent_theory: highest_theory_id = most_recent_theory["_theory_id"]
    else: highest_theory_id = 0
    theory_id = highest_theory_id + 1
    data["_theory_id"] = theory_id

    investor_theory_filter = { '$and': [
        {'_user_name': data['_user_name']},        
        {'_theory_name': data['_theory_name']}
    ]}
    already_exists = investors_theory_collection.find_one(investor_theory_filter)
    if already_exists:
        return "ALREADY INSERTED IN DATABASE", 400

    message = investors_theory_collection.insert_one(data)    
    if not message.acknowledged:
        # raise Error
        return "FAILED TO INSERT THEORY", 400
    success = {
        "message": "THEORY ADDED SUCCESSFULLY",
        "_theory_id": theory_id
    }
    return success, 200

@app.route('/investors_theory/<_theory_id>', methods=['GET'])
def get_investors_theory(_theory_id):
    investors_theory_collection = db_investors['parameters_and_weights']
    
    investor_theory_filter = {"_theory_id" : int(_theory_id)}
    message = investors_theory_collection.find_one(investor_theory_filter)
    if not message:
        return "FAILED TO FIND THEORY WHOSE ID IS "+_theory_id, 400
    return json.loads(json_util.dumps(message)), 200
    
@app.route('/investors_theory/all', methods=['GET'])
def get_all_investors_theory():
    investors_theory_collection = db_investors['parameters_and_weights']
    
    message = investors_theory_collection.find()
    if not message:
        return "NO DATA IN COLLECTION PARAMETERS IN COMPANIES DB", 400
    return json.loads(json_util.dumps(message)), 200

@app.route('/investors_theory/<_theory_id>', methods=['PUT'])
def update_investors_theory(_theory_id):
    data = request.get_json()
    investors_theory_collection = db_investors['parameters_and_weights']

    investor_theory_filter = {"_theory_id" : int(_theory_id)}
    theory_found = investors_theory_collection.find_one(investor_theory_filter)
    if not theory_found:
        return "FAILED TO FIND THEORY WHOSE ID IS "+_theory_id, 400
    
    message = investors_theory_collection.update_one(investor_theory_filter, data)    
    if not message.acknowledged:
        return "FAILED TO UPDATE THEORY WHOSE ID IS "+_theory_id, 400
    return "THEORY "+_theory_id+" UPDATED", 200

@app.route('/investors_theory/<_theory_id>', methods=['DELETE'])
def delete_investors_theory(_theory_id):
    investors_theory_collection = db_investors['parameters_and_weights']
    theory_to_remove = {"_theory_id" : int(_theory_id)}

    theory_found = investors_theory_collection.find_one(theory_to_remove)
    if not theory_found:
        return "FAILED TO FIND THEORY WHOSE ID IS "+_theory_id, 400
    
    message = investors_theory_collection.delete_one(theory_to_remove)
    if not message.acknowledged or message.deleted_count != 1:
        return "FAILED TO DELETE THEORY WHOSE ID IS "+_theory_id, 400
    return "THEORY "+_theory_id+" DELETED", 200

@app.route('/results', methods=['POST'])
def create_results():
    data = request.get_json()

    # Certify all mandatory data will be set    
    if '_theory_id' not in data: return "MISSING USER NAME", 400
    if '_company_id' not in data: return "MISSING COMPANY ID", 400
    if 'success_probability' not in data: return "MISSING SUCCESS PROBABILITY", 400
    
    investors_theory_collection = db_investors['parameters_and_weights']
    theory_filter = {"_theory_id": data['_theory_id']}
    theory_added = investors_theory_collection.find_one(theory_filter)
    if not theory_added:
        return "THEORY IS NOT IN DATABASE, PLEASE ADD THEORY FIRST"
    
    company_metrics_collection = db_companies['metrics']
    company_filter = {"_company_id" : data["_company_id"]}
    company_added = company_metrics_collection.find_one(company_filter)
    if not company_added:
        return "COMPANY IS NOT IN DATABASE, PLEASE ADD COMPANY FIRST"
    
    results_collection = db_results['results_and_comments']

    investor_theory_filter = { '$and': [
        {'_theory_id': data['_theory_id']},        
        {'_company_id': data['_company_id']}
    ]}
    already_exists = results_collection.find_one(investor_theory_filter)
    if already_exists:
        return "ALREADY INSERTED IN DATABASE", 400

    message = results_collection.insert_one(data)    
    if not message.acknowledged:
        # raise Error
        return "FAILED TO INSERT RESULT", 400
    # success = {
    #     "message": "RESULT ADDED SUCCESSFULLY",
    #     "_theory_id": data["_theory_id"],
    #     "_company_id": data["_company_id"]
    # }
    
    success = get_results(data['_theory_id'], data['_company_id'])

    return success[0], 200

@app.route('/results/single/<_theory_id>/<_company_id>', methods=['GET'])
def get_results(_theory_id, _company_id):
    results_collection = db_results['results_and_comments']
    
    results_filter = {
        "_theory_id" : int(_theory_id),
        "_company_id" : int(_company_id)        
    }
    message = results_collection.find_one(results_filter)
    if not message:
        return "FAILED TO FIND RESULTS FOR THEORY ID "+_theory_id+" AND COMPANY ID "+_company_id, 400
    return json.loads(json_util.dumps(message)), 200

@app.route('/results/theory/<_theory_id>', methods=['GET'])
def get_results_theory(_theory_id):
    results_collection = db_results['results_and_comments']
    
    results_filter = {"_theory_id" : int(_theory_id)}
    message = results_collection.find(results_filter)
    if not message:
        return "FAILED TO FIND RESULTS FOR THEORY ID "+_theory_id, 400
    return json.loads(json_util.dumps(message)), 200

@app.route('/results/company/<_company_id>', methods=['GET'])
def get_results_company(_company_id):
    results_collection = db_results['results_and_comments']
    
    results_filter = {"_company_id" : int(_company_id)}
    message = results_collection.find(results_filter)
    if not message:
        return "FAILED TO FIND RESULTS FOR COMPANY ID "+_company_id, 400
    return json.loads(json_util.dumps(message)), 200
    
@app.route('/results/all', methods=['GET'])
def get_all_results():
    results_collection = db_results['results_and_comments']
    
    message = results_collection.find()
    if not message:
        return "NO DATA IN COLLECTION PARAMETERS IN RESULTS DB", 400
    return json.loads(json_util.dumps(message)), 200

@app.route('/results/<_theory_id>/<_company_id>', methods=['PUT'])
def update_results(_theory_id, _company_id):
    data = request.get_json()
    results_collection = db_results['results_and_comments']

    results_filter = {
        "_theory_id" : int(_theory_id),
        "_company_id" : int(_company_id)        
    }
    theory_found = results_collection.find_one(results_filter)
    if not theory_found:
        return "FAILED TO FIND RESULTS FOR THEORY ID "+_theory_id+" AND COMPANY ID "+_company_id, 400
    
    message = results_collection.update_one(results_filter, data)    
    if not message.acknowledged:
        return "FAILED TO UPDATE RESULTS FOR THEORY ID "+_theory_id+" AND COMPANY ID "+_company_id, 400
    return "RESULTS FOR THEORY "+_theory_id+" COMPANY "+_company_id+" UPDATED", 200

@app.route('/results/single/<_theory_id>/<_company_id>', methods=['DELETE'])
def delete_results(_theory_id, _company_id):
    results_collection = db_results['results_and_comments']
    results_filter = {
        "_theory_id" : int(_theory_id),
        "_company_id" : int(_company_id)        
    }
    theory_found = results_collection.find_one(results_filter)
    if not theory_found:
        return "FAILED TO FIND RESULTS FOR THEORY ID "+_theory_id+" AND COMPANY ID "+_company_id, 400
    
    message = results_collection.delete_one(results_filter)
    if not message.acknowledged or message.deleted_count != 1:
        return "FAILED TO DELETE RESULTS FOR THEORY ID "+_theory_id+" AND COMPANY ID "+_company_id, 400
    return "RESULTS FOR THEORY "+_theory_id+" COMPANY "+_company_id+" DELETED", 200

@app.route('/results/theory/<_theory_id>', methods=['DELETE'])
def delete_results_theory(_theory_id):
    results_collection = db_results['results_and_comments']
    
    results_filter = {"_theory_id" : int(_theory_id)}
    result_found = results_collection.find(results_filter)
    if not result_found:
        return "FAILED TO FIND RESULTS FOR THEORY ID "+_theory_id, 400
    
    message = results_collection.delete_many(results_filter)
    if not message.acknowledged or message.deleted_count < 1:
        return "FAILED TO DELETE RESULTS FOR THEORY ID "+_theory_id, 400
    return "RESULTS FOR THEORY "+_theory_id+" DELETED", 200

@app.route('/results/company/<_company_id>', methods=['DELETE'])
def delete_results_company(_company_id):
    results_collection = db_results['results_and_comments']
    
    results_filter = {"_company_id" : int(_company_id)}
    result_found = results_collection.find(results_filter)
    if not result_found:
        return "FAILED TO FIND RESULTS FOR COMPANY ID "+_company_id, 400
    
    message = results_collection.delete_many(results_filter)
    if not message.acknowledged or message.deleted_count < 1:
        return "FAILED TO DELETE RESULTS FOR COMPANY ID "+_company_id, 400
    return "RESULTS FOR COMPANY "+_company_id+" DELETED", 200
    
@app.route('/example_investor_data/empty', methods=['GET'])
def get_empty_example_investor():
    example_collection = db_investors['examples']
    message = example_collection.find_one({"_example_id": 1, "name": "Empty example"})

    if not message: return "FAILED TO GET EMPTY EXAMPLE", 400
    return json.loads(json_util.dumps(message)), 200       

@app.route('/example_investor_data/filled', methods=['GET'])
def get_filled_example_investor():
    example_collection = db_investors['examples']
    message = example_collection.find_one({"_example_id": 2, "name": "Filled example"})

    if not message: return "FAILED TO GET FILLED EXAMPLE", 400
    return json.loads(json_util.dumps(message)), 200        

@app.route('/example_investor_data', methods=['POST'])
def create_examples_investor():
    data = request.get_json()

    # Certify all mandatory data will be set
    if '_example_id' not in data: return "MISSING EXAMPLE ID", 400
    if 'name' not in data: return "MISSING NAME", 400

    example_collection = db_investors['examples']
    message = example_collection.insert_one(data)
    
    if not message.acknowledged: return "FAILED", 400    
    # we can also return message.inserted_id, but it does not seem to show good info
    return "SUCCESS INSERTING EXAMPLE", 200








# '''This endpoint returns the object searched
# Example: /base_de_aprendizado/name/Fini'''
# @app.route('/<collection>/<attribute>/<value>', methods=['GET'])
# def get_collection_data(collection, name, attribute):
#     collection_name = db_companies[collection]
#     result = collection_name.find_one({attribute: name})
#     return result

# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":    
    # Get the database
    db_users = get_database('users')
    db_companies = get_database('companies')
    db_investors = get_database('investors_theories')
    db_results = get_database('results')

    # bp = Blueprint("bp",__name__)
    #start Flask app    
    # cors = CORS(app, support_credentials=True)    
    # app.secret_key = SECRET_KEY
    # app.config['CORS_HEADERS'] = CORS_HEADERS  
    # if TEST_MODE == 'ON': app.run(debug=True)
    # else: app.run(host='0.0.0.0', port=80, debug = True)
    app.run()