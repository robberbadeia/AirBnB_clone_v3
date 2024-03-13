#!/usr/bin/python3
'''
    RESTful API for class State
'''
from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_state():
    '''
        Method that return state in json form
    '''
    states = []
    for state in storage.all('State').values():
        states.append(state.to_dic())
    return jsonify(states)


@app_views.route('/states/<string:state_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_state_id(state_id):
    '''
        Method that return state and its id using http verb GET
    '''
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route(
    '/states/<string:state_id>',
    methods=['DELETE'],
    strict_slashes=False)
def delete_state(state_id):
    '''
        Method that delete state obj given state_id
    '''
    state = storage.get("State", state_id)
    if state is None:
        abort(404)
    state.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    '''
        Method that create new state obj
    '''
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400
    elif "name" not in request.get_json():
        return jsonify({"error": "Missing name"}), 400
    else:
        state_data = request.get_json()
        state = State(**state_data)
        state.save()
        return jsonify(state.to_dict()), 201


@app_views.route('/states/<string:states_id>',
                 methods=['PUT'],
                 strict_slashes=False)
def update_state(states_id):
    '''
        Method that update existing state object
    '''
    if not request.get_json():
        return jsonify({"error": "Not a JSON"}), 400

    obj = storage.get("State", states_id)
    if obj is None:
        abort(404)
    obj_data = request.get_json()
    obj.name = obj_data['name']
    obj.save()
    return jsonify(obj.to_dict()), 200
