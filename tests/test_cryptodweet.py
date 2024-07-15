import time
import asyncio

from dweeter import CryptoDweet


DWEET_INTERVAL = 1


def test_sync_cryptodweet():
    for use_base64 in (False, True):
        cd = CryptoDweet(b"YOUR_KEY", b"YOUR_IV", use_base64=use_base64)
        thing = "YOUR_THING" + ("_BASE64" if use_base64 else "")

        data_1 = {"DATA_1": "VALUE_1"}
        cd.dweet_for(thing, data_1)
        time.sleep(DWEET_INTERVAL)
        received_data_1 = cd.get_latest_dweet_for(thing)[0]["content"]
        time.sleep(DWEET_INTERVAL)
        assert received_data_1["DATA_1"] == data_1["DATA_1"]

        data_2 = {"DATA_2": "VALUE_2"}
        cd.dweet_for(thing, data_2)
        time.sleep(DWEET_INTERVAL)
        received_data_2 = cd.get_latest_dweet_for(thing)[0]["content"]
        time.sleep(DWEET_INTERVAL)
        assert received_data_2["DATA_2"] == data_2["DATA_2"]

        dweets = cd.get_dweets_for(thing)
        time.sleep(DWEET_INTERVAL)
        assert len(dweets) >= 2


async def async_cryptodweet():
    for use_base64 in (False, True):
        cd = CryptoDweet(b"YOUR_KEY", b"YOUR_IV", use_base64=use_base64)
        thing = "YOUR_THING" + ("_BASE64" if use_base64 else "")

        data_1 = {"DATA_1": "VALUE_1"}
        await cd.async_dweet_for(thing, data_1)
        await asyncio.sleep(DWEET_INTERVAL)
        dweet = await cd.async_get_latest_dweet_for(thing)
        received_data_1 = dweet[0]["content"]
        await asyncio.sleep(DWEET_INTERVAL)
        assert received_data_1["DATA_1"] == data_1["DATA_1"]

        data_2 = {"DATA_2": "VALUE_2"}
        await cd.async_dweet_for(thing, data_2)
        await asyncio.sleep(DWEET_INTERVAL)
        dweet = await cd.async_get_latest_dweet_for(thing)
        received_data_2 = dweet[0]["content"]
        await asyncio.sleep(DWEET_INTERVAL)
        assert received_data_2["DATA_2"] == data_2["DATA_2"]

        dweets = await cd.async_get_dweets_for(thing)
        await asyncio.sleep(DWEET_INTERVAL)
        assert len(dweets) >= 2


def test_async_cryptodweet():
    asyncio.run(async_cryptodweet())
