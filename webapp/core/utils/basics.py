"""
    very basic shared functionality. can be used anywhere
"""

import uuid

def prefixed_uuid4(prefix: str) -> str:
    """ returns a hex uuid, generated using uuid4(), with the given string prefixed """
    return "{}_{}".format(prefix, uuid.uuid4().hex)
