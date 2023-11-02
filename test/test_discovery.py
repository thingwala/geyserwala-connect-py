####################################################################################
# Copyright (c) 2023 Thingwala                                                     #
####################################################################################
from thingwala.geyserwala.connect.aio.discovery import GeyserwalaDiscoveryAsync


async def test_discovery():
    dsc = GeyserwalaDiscoveryAsync()
    res = await dsc.mdns_discover()
