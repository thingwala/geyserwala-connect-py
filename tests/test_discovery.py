####################################################################################
# Copyright (c) 2023 Thingwala                                                     #
####################################################################################
import pytest

from thingwala.geyserwala.connect.aio.discovery import GeyserwalaDiscoveryAsync


@pytest.mark.asyncio
async def test_discovery():
    dsc = GeyserwalaDiscoveryAsync()
    res = await dsc.mdns_discover()
    res[0].properties['id']
