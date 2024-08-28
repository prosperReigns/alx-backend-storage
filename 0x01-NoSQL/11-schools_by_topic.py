#!/usr/bin/env python3
"""This module implements a NoSQL DB"""


def schools_by_topic(mongo_collection, topic):
    """function returns the list of school having a specific topic"""
    return mongo_collection.find({"topics": topic})
