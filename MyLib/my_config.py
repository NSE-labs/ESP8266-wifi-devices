"""
Save and get configuration data from a file
"""
import ujson

FILENAME = 'config'

def save(obj):
    """ Saves the passed in object to FILENAME """
    file = open(FILENAME, 'w')
    file.write(ujson.dumps(obj))
    file.close()


def get():
    """
    Gets an object from FILENAME
    returns the object or None if FILENAME doesn't exist or
    if the file doesn't contain a valid object
    """
    try:
        file = open(FILENAME)
        str = file.read()
        file.close()
        obj = ujson.loads(str)
    except (OSError, ValueError):
        return None
    return obj
