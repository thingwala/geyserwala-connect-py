from unittest.mock import AsyncMock, patch

import pytest

from thingwala.geyserwala.connect.aio.client import GeyserwalaClientAsync
from thingwala.geyserwala.connect.const import (
    GEYSERWALA_MODE_HOLIDAY,
    GEYSERWALA_MODE_SETPOINT,
    GEYSERWALA_MODE_SOLAR,
    GEYSERWALA_MODE_TIMER,
)
import thingwala.geyserwala.connect.errors


@pytest.mark.asyncio
async def test_basic():
    with patch("aiohttp.ClientSession.request") as mock_req:
        response = AsyncMock()
        mock_req.return_value.__aenter__.return_value = response

        response.success = True
        response.status = 200

        async def json_success_token():
            return {"success": True, "token": "TOKEN"}

        response.json = json_success_token

        gw = GeyserwalaClientAsync("10.0.0.1")

        assert await gw.login("admin", "") is True

        VALUES = {
            "status": "Idle",
            "tank-temp": 46,
            "collector-temp": 32,
            "pump-status": False,
            "boost-demand": False,
            "setpoint": 57,
            "setpoint-max": 65,
            "element-demand": False,
            "mode": "SOLAR",
            "external-demand": False,
            "external-setpoint": 55,
            "external-disable": False,
            "id": "1234567890ABCDEF",
            "name": "Geyserwala",
            "version": "20231008-abcdef",
            "features": {
                "f-local": True,
                "f-timers": True,
                "f-collector": True,
                "f-pv-panel": False,
            },
        }

        async def json_values():
            return VALUES

        response.json = json_values

        success = await gw.update_status()
        assert success is True

        assert gw.name == "Geyserwala"
        assert gw.id == "1234567890ABCDEF"
        assert gw.version == "20231008-abcdef"
        assert gw.status == "Idle"
        assert gw.pump_status == False
        assert gw.tank_temp == 46
        assert gw.collector_temp == 32
        assert gw.boost_demand == False
        assert gw.element_demand == False
        assert gw.setpoint == 57
        assert gw.setpoint_max == 65
        assert gw.mode == GEYSERWALA_MODE_SOLAR
        assert gw.modes == [
            GEYSERWALA_MODE_SETPOINT,
            GEYSERWALA_MODE_TIMER,
            GEYSERWALA_MODE_SOLAR,
            GEYSERWALA_MODE_HOLIDAY,
        ]

        assert gw.external_setpoint == 55
        assert gw.external_demand == False
        assert gw.external_disable == False

        assert gw.has_feature("f-collector") is True
        assert gw.has_feature("f-foo") is False

        async def json_mode():
            return {"mode": "TIMER"}

        response.json = json_mode

        assert await gw.set_mode(GEYSERWALA_MODE_TIMER) is True
        assert await gw.set_mode("FOO") is False
        assert await gw.set_setpoint(65) is True
        assert await gw.set_setpoint(27) is False
        assert await gw.set_setpoint(99) is False
        assert await gw.set_boost_demand(True) is True
        assert await gw.set_boost_demand(False) is True

        assert await gw.set_external_setpoint(56) is True
        assert await gw.set_external_setpoint(27) is False
        assert await gw.set_external_setpoint(99) is False
        assert await gw.set_external_demand(True) is True
        assert await gw.set_external_disable(True) is True
        assert await gw.set_external_demand(False) is True

        TIMER1 = {
            "id": 1,
            "begin": [12, 34],
            "end": [13, 45],
            "temp": 33,
            "dow": [False, False, False, True, False, False, False],
            "flags": {"disable": False, "on-time": False},
        }

        async def json_timer():
            return TIMER1

        response.json = json_timer

        assert await gw.add_timer(TIMER1) == 1

        assert await gw.get_timer(1) == TIMER1

        async def json_timers():
            return [TIMER1]

        response.json = json_timers

        assert await gw.list_timers() == [TIMER1]

        response.json = json_timer

        assert await gw.update_timer(TIMER1) is TIMER1

        async def json_success_token():
            return {"success": True, "status": 200, "id": 1}

        response.json = json_success_token

        assert await gw.delete_timer(1) is True


@pytest.mark.asyncio
async def test_login_fail():
    with patch("aiohttp.ClientSession.request") as mock_req:
        response = AsyncMock()
        mock_req.return_value.__aenter__.return_value = response

        gw = GeyserwalaClientAsync("10.0.0.1")

        response.status = 200

        async def json_mode():
            return None

        response.json = json_mode

        await gw.login("admin", "") is False

        response.status = 401

        async def json_mode():
            return None

        response.json = json_mode

        with pytest.raises(thingwala.geyserwala.connect.errors.Unauthorized):
            await gw.login("admin", "")

        response.status = 200

        async def json_mode():
            return {"status": 200}

        response.json = json_mode

        await gw.login("admin", "") is False


@pytest.mark.asyncio
async def test_logout():
    with patch("aiohttp.ClientSession.request") as mock_req:
        response = AsyncMock()
        mock_req.return_value.__aenter__.return_value = response

        gw = GeyserwalaClientAsync("10.0.0.1")

        response.status = 200

        async def json_mode():
            return {"status": 200, "success": True}

        response.json = json_mode

        assert await gw.logout() is True

        response.status = 200

        async def json_mode():
            return None

        response.json = json_mode

        assert await gw.logout() is False

        async def json_mode():
            return {"success": False}

        response.json = json_mode

        assert await gw.logout() is False

print('foo')
