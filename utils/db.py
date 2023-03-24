__all__ = (
    'users',
)

from sqlitedict import SqliteDict

users = SqliteDict('users.db', 'users', autocommit=True)
