####################################################################################
# Copyright (c) 2023 Thingwala                                                     #
####################################################################################
import asyncio
import pytest
import os

from thingwala.geyserwala.connect.aio.client import GeyserwalaClientAsync

from thingwala.geyserwala.connect.const import (
    GEYSERWALA_MODE_TIMER,
    GEYSERWALA_MODE_HOLIDAY,
)


@pytest.fixture
def ip():
    return os.environ['TEST_IP']


@pytest.mark.asyncio
async def test_client(ip):
    gw = GeyserwalaClientAsync(ip)

    await gw.update_status()
    assert gw.name == "Geyserwala"
    gw.id
    gw.version
    gw.status
    gw.pump_status
    gw.tank_temp
    gw.collector_temp
    gw.boost_demand
    gw.element_demand
    gw.setpoint
    gw.setpoint_max
    gw.mode
    gw.modes

    gw.external_setpoint
    gw.external_demand
    gw.lowpower_enable

    gw.has_feature('f-collector')
    gw.has_feature('f-foo')

    await gw.set_mode(GEYSERWALA_MODE_TIMER)
    await gw.set_mode("FOO")
    await gw.set_setpoint(65)
    await gw.set_setpoint(99)
    await gw.set_boost_demand(True)
    await asyncio.sleep(2)
    await gw.set_boost_demand(True)
    await gw.set_mode(GEYSERWALA_MODE_HOLIDAY)

    await gw.set_external_setpoint(56)
    await gw.set_external_setpoint(99)
    await gw.set_external_demand(True)
    await gw.set_lowpower_enable(True)
    await gw.set_external_demand(False)

