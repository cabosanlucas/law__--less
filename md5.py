"""
Interface to hashlib for conversion Python 2 to Python 3
@warut-vijit
"""

import hashlib

def new(message):
    m = hashlib.sha256()
    m.update(message.encode('utf-8'))
    return m

def hexdigest(sha_obj):
    return sha_obj.hexdigest()