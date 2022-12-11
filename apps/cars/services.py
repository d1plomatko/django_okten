import os.path
from uuid import uuid1


def upload_photo(instance, file: str) -> str:
    ext = file.split('.')[-1]
    return os.path.join('cars', f'{instance.id}', f'{uuid1()}.{ext}')
