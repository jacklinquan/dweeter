import time
import json
from hashlib import sha256
from binascii import a2b_base64, b2a_base64

import basicdweet
from cryptomsg import CryptoMsg


__version__ = "0.3.0"

DEFAULT_BASE_URL = "https://dweet.io"


class DweeterError(Exception):
    pass


class CryptoDweet:
    """A class for the free dweet service with encryption.

    Initialization options:

    - `CryptoDweet()`: With default key and iv, not secure.
    - `CryptoDweet(b"YOUR_KEY")`: Only set key, with default iv.
    - `CryptoDweet(b"YOUR_KEY", b"YOUR_IV")`: Set both key and iv, strongest encryption.

    Args:
        aes_cbc_key:
            The key of AES CBC mode.
        aes_cbc_iv:
            The IV of AES CBC mode.
        base_url:
            The base url of the dweet server.
        use_base64:
            Use base64 to make dweet content dictionary more compact.
    """

    def __init__(
        self,
        aes_cbc_key: bytes = b"aes_cbc_key",
        aes_cbc_iv: bytes = b"aes_cbc_iv",
        base_url: str = DEFAULT_BASE_URL,
        use_base64: bool = False,
    ) -> None:
        self.aes_cbc_key = aes_cbc_key
        self.aes_cbc_iv = aes_cbc_iv
        self.base_url = base_url
        self.use_base64 = use_base64

    def dweet_for(self, thing: str, content_dict: dict[str, str]) -> dict:
        """The "dweet for" API.

        Args:
            thing:
                The thing name.
            content_dict:
                The content dict.

        Returns:
            The result dict of "dweet for" API.
        """
        cm = CryptoMsg(self.aes_cbc_key, self.aes_cbc_iv)
        thing_cipher = cm.encrypt_msg(thing.encode())
        thing_cipher_hex = thing_cipher.hex()

        content_dict_cipher = {
            cm.encrypt_msg(k.encode()): cm.encrypt_msg(v.encode())
            for (k, v) in content_dict.items()
        }

        if self.use_base64:
            content_dict_cipher_str = {
                b2a_base64(k)[:-1].decode(): b2a_base64(v)[:-1].decode()
                for (k, v) in content_dict_cipher.items()
            }
        else:
            content_dict_cipher_str = {
                k.hex(): v.hex() for (k, v) in content_dict_cipher.items()
            }

        return basicdweet.dweet_for(
            thing_cipher_hex,
            content_dict_cipher_str,
            base_url=self.base_url,
        )

    def _get_dweets_list(self, thing: str, api_func) -> list:
        cm = CryptoMsg(self.aes_cbc_key, self.aes_cbc_iv)
        thing_cipher = cm.encrypt_msg(thing.encode())
        thing_cipher_hex = thing_cipher.hex()

        dweets_list_cipher_str = api_func(
            thing_cipher_hex,
            base_url=self.base_url,
        )

        dweets_list = []
        for cipher_dweet in dweets_list_cipher_str:
            content_dict_cipher_str = cipher_dweet["content"]

            if self.use_base64:
                content_dict_cipher = {
                    a2b_base64(k.encode()): a2b_base64(v.encode())
                    for (k, v) in content_dict_cipher_str.items()
                }
            else:
                content_dict_cipher = {
                    bytes.fromhex(k): bytes.fromhex(v)
                    for (k, v) in content_dict_cipher_str.items()
                }

            content_dict = {
                cm.decrypt_msg(k).decode(): cm.decrypt_msg(v).decode()
                for (k, v) in content_dict_cipher.items()
            }
            decrypted_dweet = cipher_dweet
            decrypted_dweet["thing"] = thing
            decrypted_dweet["content"] = content_dict
            dweets_list.append(decrypted_dweet)

        return dweets_list

    def get_latest_dweet_for(self, thing: str) -> list:
        """The "get latest dweet for" API.

        Args:
            thing:
                The thing name.

        Returns:
            The result list of dict of "get latest dweet for" API.
        """
        return self._get_dweets_list(thing, basicdweet.get_latest_dweet_for)

    def get_dweets_for(self, thing: str) -> list:
        """The "get dweets for" API.

        Args:
            thing:
                The thing name.

        Returns:
            The result list of dict of "get dweets for" API.
        """
        return self._get_dweets_list(thing, basicdweet.get_dweets_for)

    async def async_dweet_for(self, thing: str, content_dict: dict[str, str]) -> dict:
        """The async "dweet for" API.

        The arguments have the same meaning as in `dweet_for`.
        """
        cm = CryptoMsg(self.aes_cbc_key, self.aes_cbc_iv)
        thing_cipher = cm.encrypt_msg(thing.encode())
        thing_cipher_hex = thing_cipher.hex()

        content_dict_cipher = {
            cm.encrypt_msg(k.encode()): cm.encrypt_msg(v.encode())
            for (k, v) in content_dict.items()
        }

        if self.use_base64:
            content_dict_cipher_str = {
                b2a_base64(k)[:-1].decode(): b2a_base64(v)[:-1].decode()
                for (k, v) in content_dict_cipher.items()
            }
        else:
            content_dict_cipher_str = {
                k.hex(): v.hex() for (k, v) in content_dict_cipher.items()
            }

        return await basicdweet.async_dweet_for(
            thing_cipher_hex,
            content_dict_cipher_str,
            base_url=self.base_url,
        )

    async def _async_get_dweets_list(self, thing: str, api_func) -> list:
        cm = CryptoMsg(self.aes_cbc_key, self.aes_cbc_iv)
        thing_cipher = cm.encrypt_msg(thing.encode())
        thing_cipher_hex = thing_cipher.hex()

        dweets_list_cipher_str = await api_func(
            thing_cipher_hex,
            base_url=self.base_url,
        )

        dweets_list = []
        for cipher_dweet in dweets_list_cipher_str:
            content_dict_cipher_str = cipher_dweet["content"]

            if self.use_base64:
                content_dict_cipher = {
                    a2b_base64(k.encode()): a2b_base64(v.encode())
                    for (k, v) in content_dict_cipher_str.items()
                }
            else:
                content_dict_cipher = {
                    bytes.fromhex(k): bytes.fromhex(v)
                    for (k, v) in content_dict_cipher_str.items()
                }

            content_dict = {
                cm.decrypt_msg(k).decode(): cm.decrypt_msg(v).decode()
                for (k, v) in content_dict_cipher.items()
            }
            decrypted_dweet = cipher_dweet
            decrypted_dweet["thing"] = thing
            decrypted_dweet["content"] = content_dict
            dweets_list.append(decrypted_dweet)

        return dweets_list

    async def async_get_latest_dweet_for(self, thing: str) -> list:
        """The async "get latest dweet for" API.

        The arguments have the same meaning as in `get_latest_dweet_for`.
        """
        return await self._async_get_dweets_list(
            thing,
            basicdweet.async_get_latest_dweet_for,
        )

    async def async_get_dweets_for(self, thing: str) -> list:
        """The async "get dweets for" API.

        The arguments have the same meaning as in `get_dweets_for`.
        """
        return await self._async_get_dweets_list(
            thing,
            basicdweet.async_get_dweets_for,
        )


class Dweeter:
    """A class for encrypted messaging through the free dweet service.

    Args:
        mailbox:
            A virtual mailbox name.
        key:
            The key to the virtual mailbox.
        debug:
            If it is `True`, exceptions will be printed.
            Otherwise exceptions will be swallowed silently.
        base_url:
            The base url of the dweet server.
        use_base64:
            Use base64 to make dweet content dictionary more compact.

    Notes:
        With the same `mailbox`,
        when using a different `key` or different `use_base64` settings,
        it actually creates a different thing name in dweet service.
    """

    utc_format = "{:04d}-{:02d}-{:02d}T{:02d}:{:02d}:{:02d}.000Z"

    def __init__(
        self,
        mailbox: str = "default_mailbox",
        key: str = "default_key",
        debug: bool = False,
        base_url: str = DEFAULT_BASE_URL,
        use_base64: bool = False,
    ) -> None:
        self.mailbox = mailbox
        hash_result = sha256(key.encode()).digest()
        cd_key = hash_result[:16]
        cd_iv = hash_result[16:]
        if use_base64:
            cd_key, cd_iv = cd_iv, cd_key
        self._cd = CryptoDweet(
            cd_key,
            cd_iv,
            base_url=base_url,
            use_base64=use_base64,
        )
        self.debug = debug
        self.latest = None

    def send_data(self, data_dict: dict) -> dict:
        """Send `data_dict` to the mailbox.

        Args:
            data_dict:
                The data dictionary to send to the mailbox.
                This dictionary must be json compatible.
                There are 2 keys reserved for data_dict.
                One is `created_time`, the dweet service time.
                The other is `remote_time`, the local time of the remote device.

        Returns:
            The dweet transaction dict returned from dweet service.
            It should include the keys of `thing`, `content`, `created`
            and `transaction`.
        """
        if not isinstance(data_dict, dict):
            raise DweeterError("`data_dict` must be an instance of dict.")

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

    def get_new_data(self) -> dict:
        """Receive the latest and new `data_dict` from the mailbox.

        Returns:
            The latest and new data dictionary from the mailbox.
            None will be returned if the latest `data_dict` is old.
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

    async def async_send_data(self, data_dict: dict) -> dict:
        """Send `data_dict` to the mailbox asynchronously.

        The arguments have the same meaning as in `send_data`.
        """
        if not isinstance(data_dict, dict):
            raise DweeterError("`data_dict` must be an instance of dict.")

        time_string = self.utc_format.format(*(time.gmtime()[:6]))
        data_dict_copy = data_dict.copy()
        data_dict_copy["remote_time"] = time_string
        data_json = json.dumps(data_dict_copy)
        res = None

        try:
            res = await self._cd.async_dweet_for(self.mailbox, {time_string: data_json})
        except Exception as exc:
            if self.debug:
                print(type(exc).__name__, exc)

        return res

    async def async_get_new_data(self) -> dict:
        """Receive the latest and new `data_dict` from the mailbox asynchronously.

        The arguments have the same meaning as in `get_new_data`.
        """
        try:
            res = await self._cd.async_get_latest_dweet_for(self.mailbox)
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
