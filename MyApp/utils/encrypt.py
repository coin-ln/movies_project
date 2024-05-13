import hashlib
from movies_project.settings import SECRET_KEY
def md5(data_string):
    salt=SECRET_KEY
    obj = hashlib.md5(salt.encode('utf-8'))
    obj.update(data_string.encode('utf-8'))
    return obj.hexdigest()