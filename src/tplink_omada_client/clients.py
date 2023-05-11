"""
Definitions for Omada Clients
"""

from typing import Any, Optional
from datetime import datetime, timezone, timedelta
from .devices import OmadaApiData
from .definitions import (
    ConnectedClientType,
    WifiMode,
    RadioID,
    AuthStatus,
)


class OmadaClientDevice(OmadaApiData):
    """Details of a client device connnected to the network.
       If the device is online, this is a base class for either
       OmadaWirelessClientDevice or OmadaWiredClientDevice."""

    @property
    def mac(self) -> str:
        """The MAC address of the device."""
        return self._data["mac"]

    @property
    def name(self) -> str:
        """The client name."""
        return self._data["name"]

    @property
    def host_name(self) -> Optional[str]:
        """The Host name, device name."""
        if self.active:
            return self._data["hostName"]
        return None

    @property
    def device_type(self) -> str:
        """The device type: i.e. iphone, android, pc..."""
        return self._data["deviceType"]

    @property
    def ip_address(self) -> Optional[str]:
        """IP address of the device."""
        # The device can be missing an IP if it's offline
        #  or if it hasn't been assigned one yet.
        if self.active and "ip" in self._data:
            return self._data["ip"]
        return None

    @property
    def wireless(self) -> Optional[bool]:
        """Whether the device is connected via an AP."""
        if self.active:
            return self._data["wireless"]
        return False

    @property
    def connected_type(self) -> Optional[str]:
        """The type of device connected. Its value can be "ap", "gateway", and "switch"."""
        if self.active:
            return self._data["connectDevType"]
        return None

    @property
    def type(self) -> Optional[ConnectedClientType]:
        """Connected type."""
        if self.active:
            return ConnectedClientType(self._data["connectType"])
        return None

    @property
    def activity(self) -> Optional[int]:
        """Real-time downlink rate (Byte/s) at time of creation."""
        if self.active:
            return self._data["activity"]
        return 0

    @property
    def traffic_down(self) -> Optional[int]:
        """Downlink traffic (Byte)"""
        if self.active:
            return self._data["trafficDown"]
        return 0

    @property
    def traffic_down_packet(self) -> Optional[int]:
        """Number of downstream packets."""
        if self.active:
            return self._data["downPacket"]
        return 0

    @property
    def traffic_up(self) -> Optional[int]:
        """Upstream traffic (Byte)"""
        if self.active:
            return self._data["trafficUp"]
        return 0

    @property
    def traffic_up_packet(self) -> Optional[int]:
        """Number of upstream packets."""
        if self.active:
            return self._data["upPacket"]
        return 0

    @property
    def uptime(self) -> int:
        """Uptime of the device, in seconds."""
        if self.active:
            return self._data["uptime"]
        return 0

    @property
    def last_seen(self) -> datetime:
        """Last seen time"""
        # Omada API returns timestamp in ms.
        return datetime.fromtimestamp(self._data["lastSeen"]/1000)

    @property
    def auth_status(self) -> Optional[AuthStatus]:
        """Authentication Status."""
        if self.active:
            return AuthStatus(self._data["authStatus"])
        return None

    @property
    def is_guest(self) -> Optional[bool]:
        """Whether it is a guest client device."""
        if self.active:
            return self._data["guest"]
        return None

    @property
    def active(self) -> bool:
        """Whether the device is active."""
        return self._data["active"]

class OmadaWirelessClientDevice(OmadaClientDevice):

    @property
    def ssid(self) -> str:
        """Client connected SSID name."""
        return self._data["ssid"]

    @property
    def wifi_mode(self) -> WifiMode:
        """Mode of wifi connection."""
        return WifiMode(self._data["wifiMode"])
    
    @property
    def ap_name(self) ->str :
        """Name of connected AP."""
        return self._data["apName"]
    
    @property
    def ap_mac(self) -> str:
        """MAC address of connected AP."""
        return self._data["apMac"]
    
    @property
    def radio_id(self) -> RadioID:
        """Radio Band for wifi connection."""
        return RadioID(self._data["radioId"])

    @property
    def channel(self) -> int:
        """Actual client channel."""
        return self._data["channel"]
    
    @property
    def rx_rate(self) -> int:
        """Uplink negotiation rate (Kbit/s)"""
        return self._data["rxRate"]

    @property
    def tx_rate(self) -> int:
        """Downlink negotiation rate (Kbit/s)"""
        return self._data["txRate"]

    @property
    def power_save(self) -> bool:
        """true: Power save mode enabled"""
        return self._data["powerSave"]

    @property
    def rssi(self) -> int:
        """Signal strength, unit: dBm"""
        return self._data["rssi"]

    @property
    def signal_level(self) -> int:
        """Signal strength percentage, value range [0, 100]"""
        return self._data["signalLevel"]

    @property
    def signal_rank(self) -> int:
        """Signal strength level, value range [0, 5]"""
        return self._data["signalRank"]

class OmadaWiredClientDevice(OmadaClientDevice):

    @property
    def switch_mac(self) -> Optional[str]:
        """MAC address of the connected switch"""
        if self.connected_type == "switch":
            return self._data["switchMac"]
        return ""

    @property
    def switch_name(self) -> Optional[str]:
        """Name of connected switch."""
        if self.connected_type == "switch":
            return self._data["switchName"]
        return ""
    
    @property
    def gateway_mac(self) -> Optional[str]:
        """MAC address of the connected Gateway."""
        if self.connected_type == "gateway":
            return self._data["gatewayMac"]
        return ""
    
    @property
    def gateway_name(self) -> Optional[str]:
        """Name of the connected Gateway."""
        if self.connected_type == "gateway":
            return self._data["gatewayName"]
        return ""

    @property
    def network_name(self) -> str:
        """Network name."""
        return self._data["networkName"]

    @property
    def dot1x_identity(self) -> str:
        """802.1x authentication identity"""
        return self._data["dot1xIdentity"]

    @property
    def dot1x_vlan(self) -> str:
        """Network name corresponding to the VLAN obtained by 802.1x D-VLAN"""
        return self._data["dot1xVlan"]

    @property
    def port(self) -> str:
        """Port ID"""
        return self._data["port"]

def CreateOmadaClientDevice(data: dict[str, Any]) -> OmadaClientDevice:
    if not data['active']:
        return OmadaClientDevice(data)
    elif data["wireless"]:
        return OmadaWirelessClientDevice(data)
    else:
        return OmadaWiredClientDevice(data)
