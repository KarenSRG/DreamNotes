from passlib.context import CryptContext

# Инициализация контекста для хэширования паролей
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """
    Хэширует пароль с использованием bcrypt.
    """
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Проверяет пароль с хэшированным паролем.
    """
    return pwd_context.verify(plain_password, hashed_password)
