"""A python module for messaging through the free dweet service.

- Author: Quan Lin
- License: MIT
"""

__version__ = "0.1.0"
__all__ = ["DweeterError", "Dweeter"]

import time
import json
from hashlib import sha256
from cryptodweet import CryptoDweet, to_bytes, from_bytes


class DweeterError(Exception):
    pass


class Dweeter:
    """A class for messaging through the free dweet service.

    Parameters
    ----------
    mailbox : str
        A virtual mailbox through the free dweet service.
    key : str
        The key to the virtual mailbox.
    debug: bool, optional
        If it is `True`, exceptions will be printed.
        Otherwise exceptions will be swallowed silently.
        (default is `False`)

    Attributes
    ----------
    mailbox : str
        A virtual mailbox through the free dweet service.
    latest : dict
        The latest received data dictionary.
    debug : bool
        If it is `True`, exceptions will be printed.
        Otherwise exceptions will be swallowed silently.

    Methods
    -------
    send_data(data_dict)
        Send the data_dict to the mailbox.
    get_new_data()
        Receive the latest and new data_dict from the mailbox.

    Notes
    -----
    With the same mailbox and a different key,
    it actually creates a different virtual mailbox.
    """

    utc_format = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}.000Z"

    def __init__(self, mailbox="default mailbox", key="default key", debug=False):
        self.mailbox = mailbox
        hash_result = sha256(to_bytes(key)).digest()
        cd_key = hash_result[:16]
        cd_iv = hash_result[16:]
        self._cd = CryptoDweet(cd_key, cd_iv)
        self.debug = debug
        self.latest = None

    def send_data(self, data_dict):
        """Send the data_dict to the mailbox.

        Parameters
        ----------
        data_dict : dict
            The data dictionary to send to the mailbox.
            This dictionary must be json compatible.
            There are 2 keys reserved for data_dict.
            One is "created_time", the dweet service time.
            The other is "remote_time", the local time of the remote device.

        Returns
        -------
        dict
            The dweet transaction dict returned from dweet service.
            It should include the keys of 'thing', 'content', 'created'
            and 'transaction'.
        """

        if not isinstance(data_dict, dict):
            raise DweeterError("data_dict must be instance of dict.")

        time_string = self.utc_format.format(*(time.gmtime()[:6]))
        data_dict_copy = data_dict.copy()
        data_dict_copy["remote_time"] = time_string
        data_json = json.dumps(data_dict_copy)
        res = None

        try:
            res = self._cd.dweet_for(self.mailbox, {time_string: data_json})
        except Exception as exc:
            if self.debug:
                print(type(exc).__name__, exc)

        return res

    def get_new_data(self):
        """Receive the latest and new data_dict from the mailbox.

        Returns
        -------
        dict
            The latest and new data dictionary from the mailbox.
            None will be returned if the latest data_dict is old.
        """

        try:
            res = self._cd.get_latest_dweet_for(self.mailbox)
            content = res[0]["content"]
            created = res[0]["created"]
            time_string = list(content.keys())[0]
            data_json = list(content.values())[0]
            data_dict = json.loads(data_json)
            data_dict["created_time"] = created
            if data_dict["remote_time"] != time_string:
                raise DweeterError("Received data is compromised!")
        except Exception as exc:
            if self.debug:
                print(type(exc).__name__, exc)
            return None
        else:
            if (self.latest is None) or (
                self.latest["created_time"] < data_dict["created_time"]
            ):
                self.latest = data_dict
                return data_dict
            else:
                return None
