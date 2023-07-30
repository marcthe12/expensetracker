from dataclasses import dataclass
from sqlalchemy import Text, TypeDecorator
from werkzeug.security import check_password_hash, generate_password_hash


@dataclass(eq=False)
class PasswordHash:
    """
    Generate hash for password storage. It wraps arround the werkzeug.security
    module.
    """

    hash: str

    def __eq__(self, candidate) -> bool:
        return check_password_hash(self.hash, candidate)

    @classmethod
    def new(cls, password: str, method: str = "pbkdf2", salt_length: int = 16):
        """Wrapper over generate_password"""
        hashed_password = generate_password_hash(password, method, salt_length)
        return cls(hashed_password)


class Password(TypeDecorator):
    """The SQLAlchemy Addapter for PasswordHash"""

    impl = Text

    def process_bind_param(self, value, dialect) -> str | None:
        if value is not None:
            if isinstance(value, PasswordHash):
                return value.hash
            raise ValueError("Invalid value type. Expected PasswordHash object.")
        return None

    def process_result_value(self, value: str, dialect) -> PasswordHash | None:
        if value is not None:
            return PasswordHash(value)
        return None

    def coerce_compared_value(self, op, value):
        if isinstance(value, PasswordHash):
            return value.hash
        return super().coerce_compared_value(op, value)
