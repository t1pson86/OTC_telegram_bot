import uuid

def uniq_generation():
    uniq_id = uuid.uuid4().hex[:11]
    return uniq_id

