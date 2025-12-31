import hashlib
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    # SHA256 ilə 32 byte-ə sal
    sha = hashlib.sha256(password.encode("utf-8")).hexdigest()
    
    # bcrypt
    return pwd_context.hash(sha)


def verify_password(password: str, hashed_password: str) -> bool:
    sha = hashlib.sha256(password.encode("utf-8")).hexdigest()
    return pwd_context.verify(sha, hashed_password)
