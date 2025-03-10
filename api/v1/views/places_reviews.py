#!/usr/bin/python3
""" places reviews"""

from api.v1.views import app_views
from flask import Flask, Blueprint, jsonify, abort, make_response, request
from models import storage, place, review


@app_views.route('/reviews', methods=['GET'], strict_slashes=False)
def reviews():
    """defines reviews"""

    reviews = []
    my_reviews = storage.all('Review').values()
    for review in my_reviews:
        reviews.append(review.to_dict())
    return jsonify(reviews)


@app_views.route('/places/<string:place_id>/reviews', methods=['GET'], strict_slashes=False)
def reviews_place_id(place_id):
    """Returns an object into a valid JSON"""

    reviews = []
    the_place = storage.get('Place', place_id)
    if the_place is None:
        abort(404)
    for my_review in the_place.reviews:
        reviews.append(my_review.to_dict())
    return jsonify(reviews)


@app_views.route('/reviews/<string:review_id>', methods=['GET'], strict_slashes=False)
def review_id(review_id):
    """Return  a Review object"""

    my_review = storage.get('Review', review_id)
    if my_review is None:
        abort(404)
    return jsonify(my_review.to_dict())


@app_views.route('/reviews/<string:review_id>', methods=['DELETE'], strict_slashes=False)
def review_id_delete(review_id):
    """Deletes a Review object"""

    my_review = storage.get('Review', review_id)
    if my_review is None:
        abort(404)
    my_review.delete()
    storage.save()
    return jsonify({})


@app_views.route('places/<place_id>/reviews', methods=['POST'], strict_slashes=False)
def create_review(place_id):
    """Creates a Review object"""

    the_place = storage.get('Place', place_id)
    if the_place is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    if 'user_id' not in request.json:
        abort(400, 'Missing user_id')
    if 'text' not in request.json:
        abort(400, 'Missing text')
    my_user = storage.get('User', request.json.get('user_id', ""))
    if my_user is None:
        abort(404)
    req = request.get_json(silent=True)
    req['place_id'] = place_id
    my_review = review.Review(**req)
    storage.new(my_review)
    my_review.save()
    return make_response(jsonify(my_review.to_dict()), 201)


@app_views.route('/reviews/<string:review_id>', methods=['PUT'], strict_slashes=False)
def update_review(review_id):
    """update review"""

    my_review = storage.get('Review', review_id)
    if my_review is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    for rq in request.get_json(silent=True):
        if rq not in ['id', 'user_id', 'place_id', 'created_at', 'updated_at']:
            setattr(my_review, rq, request.json[rq])
    my_review.save()
    return jsonify(my_review.to_dict())


if __name__ == "__main__":
    pass
