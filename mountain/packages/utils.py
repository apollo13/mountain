from hashlib import sha1

def get_hash(type, name, version, relations):
    digest = sha1("[%d %s %s]" % (type, name, version))
    relations.sort()
    for pair in relations:
        digest.update("[%d %s]" % pair)
    return digest.hexdigest()
