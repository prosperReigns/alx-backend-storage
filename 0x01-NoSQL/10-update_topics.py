#!/usr/bin/env python3
"""This module implements a NoSQL DB"""


def update_topics(mongo_collection, name, topics):
    """function changes all topics of a school document based on the name

    Args:
        mongo_collection: The pymongo collection object.
        name (str): The school name to update.
        topics (list of str): The list of topics approached in the school.
    """
    mongo_collection.update_many({"name": name}, {'$set': {"topics": topics}})
