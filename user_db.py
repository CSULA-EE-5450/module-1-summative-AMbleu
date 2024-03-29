from typing import Tuple, Dict
import secrets
import nacl.pwhash


class UserDB(object):
    def __init__(self):
        self._accounts: Dict[str, bytes] = {}

    def create_user(self, username: str) -> Tuple[str, str]:
        """
        Creates a user and returns a automatically-generated token (password)
        for the user.  You can generate this token using secrets.token_urlsafe()

        Only the one-way hash is stored in self._accounts.

        To make hashes, read: https://pynacl.readthedocs.io/en/latest/password_hashing/
        In particular, you want to use the nacl.pwhash.str() function.
        NOTE: str expects passwords in bytes!  Use the str type's encode() function
        or the bytes type's decode() function to help you convert.

        :raises: ValueError if the username already exists
        :param username: desired username
        :return: (username, password_token)
        """

        if username in self._accounts.keys():
            raise ValueError("Username already exists")

        password_token = str.encode(secrets.token_urlsafe())
        self._accounts[username] = nacl.pwhash.str(password_token)
        password_token = bytes.decode(password_token)

        return username, password_token
        pass

    def is_valid(self, username: str, password) -> bool:
        """
        Check whether the given username and password match a user
        present in the UserDB.  The hash of the input password is
        compared to the stored hash.

        See what you can call in nacl.pwhash to verify an input password.

        :param username:
        :param password:
        :return: True if the credentials are valid, False if not.
        """
        password_bytes = str.encode(password)

        try:
            if username in self._accounts.keys() and nacl.pwhash.verify(self._accounts[username], password_bytes):
                return True
        except:
            return False
        pass
