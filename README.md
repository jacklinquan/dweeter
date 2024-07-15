# Dweeter

[![PyPI version][pypi_img]][pypi_link]
[![Downloads][downloads_img]][downloads_link]

  [pypi_img]: https://badge.fury.io/py/dweeter.svg
  [pypi_link]: https://badge.fury.io/py/dweeter
  [downloads_img]: https://pepy.tech/badge/dweeter
  [downloads_link]: https://pepy.tech/project/dweeter

[Documentation](https://jacklinquan.github.io/dweeter)

Encrypted messaging through the free dweet service.
Dweet is a simple machine-to-machine (M2M) service from [dweet.io](https://dweet.io).

It also can be used in MicroPython.

---

## Installation

### Synchronous Programming

```shell
pip install dweeter
```

### Asynchronous Programming

```shell
pip install dweeter[aiohttp]
```

---

## Usage

### Synchronous Programming

<details open><summary>Code</summary>

```python
import time
from dweeter import Dweeter

dwtr = Dweeter("MAILBOX_NAME", "KEY_TO_MAILBOX")

print(dwtr.send_data({"DATA_1": "VALUE_1"}))
time.sleep(2)
print(dwtr.get_new_data())
time.sleep(2)
print(dwtr.send_data({"DATA_2": "VALUE_2"}))
time.sleep(2)
print(dwtr.get_new_data())
```
</details>

<details open><summary>Output</summary>

```
{'thing': '42e6ae04e842cadca8a814fea06bcf6d', 'created': '2024-07-15T05:11:32.709Z', 'content': {'904b0c7d2cfe0dd2501e7f25101fb92457f58052e8526dafb38b883438896980': '4c03f62878dd6d9befdc92e00a2a1bd4906c9590838f7758062e37b99c05b696cb01b729f7c9faa6962726e5dc6a4b1ad522dd0dceb3870106a67ebaedf9868b87548e04347fbc721e152f03ac405fb1'}, 'transaction': 'c8f956a5-e516-4ad4-afa5-5035d4206179'}
{'DATA_1': 'VALUE_1', 'remote_time': '2024-07-15T05:11:31.000Z', 'created_time': '2024-07-15T05:11:32.709Z'}
{'thing': '42e6ae04e842cadca8a814fea06bcf6d', 'created': '2024-07-15T05:11:38.580Z', 'content': {'904b0c7d2cfe0dd2501e7f25101fb924cb74208c05dc802c752e5e2717f4c717': '10753b950ecdcbf5a9b7cd82f82c3bac7d5b522a175897e2db32457d6f373cbc2fe8f7ef551284de110e6b9abfa058404b8f9d4126e18d3c32e137e5902f298c722cf8261460613602484dae350cb8f6'}, 'transaction': '2dcec037-9b02-4dc2-a6c1-26cc0beb4e03'}
{'DATA_2': 'VALUE_2', 'remote_time': '2024-07-15T05:11:37.000Z', 'created_time': '2024-07-15T05:11:38.580Z'}
```
</details>

### Asynchronous Programming

<details><summary>Code</summary>

```python
import asyncio
from dweeter import Dweeter

async def async_main():
    dwtr = Dweeter("MAILBOX_NAME", "KEY_TO_MAILBOX")

    print(await dwtr.async_send_data({"DATA_1": "VALUE_1"}))
    await asyncio.sleep(2)
    print(await dwtr.async_get_new_data())
    await asyncio.sleep(2)
    print(await dwtr.async_send_data({"DATA_2": "VALUE_2"}))
    await asyncio.sleep(2)
    print(await dwtr.async_get_new_data())

asyncio.run(async_main())
```
</details>

<details><summary>Output</summary>

```
{'thing': '42e6ae04e842cadca8a814fea06bcf6d', 'created': '2024-07-15T05:12:20.059Z', 'content': {'0d93e2a03ea4fea5741276e310398b65e6f55f0456d6d2bb74b01ffca22bf9ba': '4c03f62878dd6d9befdc92e00a2a1bd4906c9590838f7758062e37b99c05b696cb01b729f7c9faa6962726e5dc6a4b1a3b18b95d5e6552c4b61913acf2861b0e3a45a4113ac684bc5a08bf5a82d65816'}, 'transaction': 'e5b08537-2c14-4ce9-be72-5d804607ce26'}
{'DATA_1': 'VALUE_1', 'remote_time': '2024-07-15T05:12:19.000Z', 'created_time': '2024-07-15T05:12:20.059Z'}
{'thing': '42e6ae04e842cadca8a814fea06bcf6d', 'created': '2024-07-15T05:12:25.941Z', 'content': {'0d93e2a03ea4fea5741276e310398b6557ef5805e83d93aa199097fd01b51821': '10753b950ecdcbf5a9b7cd82f82c3bac7d5b522a175897e2db32457d6f373cbc2fe8f7ef551284de110e6b9abfa05840066efe7671423a88111a87a6a58076595fee9457ed0fa115dc463cf66c031017'}, 'transaction': 'b025efed-16ab-46ba-96f3-4df72ef5dcdf'}
{'DATA_2': 'VALUE_2', 'remote_time': '2024-07-15T05:12:25.000Z', 'created_time': '2024-07-15T05:12:25.941Z'}
```
</details>

---

## Test

```shell
python -m pytest
```

---

## Build documentation

```shell
mkdocs build
```

---

## Change

- v0.3.0:
    - `CryptoDweet` class is added.
    - Asynchronous methods are added for asynchronous programming.
    - Dweet content dictionary can be encoded with base64 to be more compact.

---

## On messaging security

The free dweet service is public.
By "public", it means:

- Every one on Internet can see what you are sending.
- Every one can send something for the same "thing" name to confuse you.

The publicly exposed user information:

- The "thing" name, which you can think of as the unique virtual mailbox name.
- The keys of the "content" dictionary.
- The values of the "content" dictionary.

The dweeter module wraps the contents as a single key-value pair.
So there is only one key and one value in the "content" dictionary.
And the "thing" name and the "content" dictionary are encrypted.
So no one knows what they mean.

Without knowing what the information means,
potential attackers can still send something for the same "thing" name.
Because the "content" dictionary is encrypted,
the only way to do this is to capture a bunch of messages
and send them randomly.
The key and the value of the "content" dictionary both include
the same time stamp.
A mismatch of them will result in an error that is handled by dweeter.
But a copy of the whole "content" dictionary could
still be passed on to the receiver.
This is often referred to as "replay attack".

The decrypted user data dictionary includes 2 extra key-value pairs:

- "created_time", the timestamp from the dweet service.
- "remote_time", the timestamp from the sending device.

You can compare these two timestamps to decide if a "replay attack" happened.
On a micropython device, you can use `ntptime.settime()` to set the local time.
Be aware of a normal gap between "created_time" and "remote_time".
On a PC I observed 4 to 5 seconds difference.
On a micropython device I observed 8 to 9 seconds difference.
This time difference could vary from case to case.
