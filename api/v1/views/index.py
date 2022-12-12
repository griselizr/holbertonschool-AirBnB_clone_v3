#!/usr/bin/python3
""" View index: status message"""


import models
from flask import Flask, Blueprint, jsonify
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def _status():
    """returns a JSON file with Status: OK"""

    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def count():
    """ Returns count of objects by type """

    utilities_dic = {}

    classes = {
        "Amenity": "amenities",
        "City": "cities",
        "Place": "places",
        "Review": "reviews",
        "State": "states",
        "User": "users"}

    for k, val in classes.items():
        utilities_dic[val] = models.storage.count(k)
        return jsonify(utilities_dic)
