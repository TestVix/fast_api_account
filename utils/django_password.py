# utils/django_password.py

import hashlib
import binascii

def verify_django_password(raw_password: str, hashed_password: str) -> bool:
    """
    Django formatidagi passwordni tekshiradi:
    format: algorithm$iterations$salt$hash
    """
    algorithm, iterations, salt, hash_val = hashed_password.split('$')

    dk = hashlib.pbkdf2_hmac(
        'sha256',
        raw_password.encode(),
        salt.encode(),
        int(iterations)
    )
    calc_hash = binascii.hexlify(dk).decode()

    return calc_hash == hash_val
