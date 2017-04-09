"""
Interface to hashlib for conversion Python 2 to Python 3
@warut-vijit
"""

import hashlib

def new(message):
    m = hashlib.sha256()
    return m.update(message.encode('utf-8'))

def hexdigest(sha_obj):
    return sha_obj.hexdigest()