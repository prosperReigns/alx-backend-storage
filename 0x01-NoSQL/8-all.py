#!/usr/bin/env python3
"""This module implements a NoSQL DB"""


def list_all(mongo_collection):
    """function lists all documents in a collection"""
    return mongo_collection.find()
