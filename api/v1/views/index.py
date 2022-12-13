#!/usr/bin/python3
""" View index: status message"""

from flask import Flask, Blueprint, jsonify
from api.v1.views import app_views


@app_views.route('/status', strict_slashes=False)
def stats():
    """returns a JSON file with Status: OK"""

    return jsonify({"status": "OK"})


@app_views.route('/stats', strict_slashes=False)
def count():
    """ Returns count of objects by type """

    the_Dic = {}

    classes = {
        "Amenity": "amenities",
        "City": "cities",
        "Place": "places",
        "Review": "reviews",
        "State": "states",
        "User": "users"
    }

    for k, v in classes.items():
        the_Dic[v] = models.storage.count(k)
    return jsonify(the_Dic)
