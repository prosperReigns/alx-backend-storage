#!/usr/bin/env python3
"""This module implements a NoSQL DB"""


def insert_school(mongo_collection, **kwargs):
    """function inserts a new document in a collection based on kwargs"""
    result = mongo_collection.insert_one(kwargs)
    return result.inserted_id
