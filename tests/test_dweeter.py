import time
import asyncio

from dweeter import Dweeter


DWEET_INTERVAL = 1


def test_sync_dweeter():
    for use_base64 in (False, True):
        dwtr = Dweeter("MAILBOX_NAME", "KEY_TO_MAILBOX", use_base64=use_base64)

        data_1 = {"DATA_1": "VALUE_1"}
        dwtr.send_data(data_1)
        time.sleep(DWEET_INTERVAL)
        received_data_1 = dwtr.get_new_data()
        time.sleep(DWEET_INTERVAL)
        assert received_data_1["DATA_1"] == data_1["DATA_1"]

        data_2 = {"DATA_2": "VALUE_2"}
        dwtr.send_data(data_2)
        time.sleep(DWEET_INTERVAL)
        received_data_2 = dwtr.get_new_data()
        time.sleep(DWEET_INTERVAL)
        assert received_data_2["DATA_2"] == data_2["DATA_2"]


async def async_dweeter():
    for use_base64 in (False, True):
        dwtr = Dweeter("MAILBOX_NAME", "KEY_TO_MAILBOX", use_base64=use_base64)

        data_1 = {"DATA_1": "VALUE_1"}
        await dwtr.async_send_data(data_1)
        await asyncio.sleep(DWEET_INTERVAL)
        received_data_1 = await dwtr.async_get_new_data()
        await asyncio.sleep(DWEET_INTERVAL)
        assert received_data_1["DATA_1"] == data_1["DATA_1"]

        data_2 = {"DATA_2": "VALUE_2"}
        await dwtr.async_send_data(data_2)
        await asyncio.sleep(DWEET_INTERVAL)
        received_data_2 = await dwtr.async_get_new_data()
        await asyncio.sleep(DWEET_INTERVAL)
        assert received_data_2["DATA_2"] == data_2["DATA_2"]


def test_async_dweeter():
    asyncio.run(async_dweeter())
