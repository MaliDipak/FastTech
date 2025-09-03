import bcrypt


def get_hash_password(password):
    return bcrypt.hashpw(password=str(password).encode("utf-8"), salt=bcrypt.gensalt()).decode("utf-8")
