"""Implementation for 'clients' command"""

from argparse import _SubParsersAction
from .config import get_target_config, to_omada_connection
from .util import dump_raw_data, get_target_argument
from ..clients import OmadaWiredClientDevice, OmadaWirelessClientDevice

async def command_clients(args) -> int:
    """Executes 'clients' command"""
    controller = get_target_argument(args)
    config = get_target_config(controller)

    async with to_omada_connection(config) as client:
        site_client = await client.get_site_client(config.site)
        for device in await site_client.get_client_devices():
            if isinstance(device, OmadaWirelessClientDevice):
                if device.ip_address:
                    print(f"{device.name:<22} {device.ip_address:>15} {device.ssid:<18} {device.activity:>8} Bytes/s {device.uptime:>6} s")
                else:
                    print(f"{device.name:<22} {'--':^15} {device.ssid:<18} {device.activity:>8} Bytes/s {device.uptime:>6} s")
            else:
                if device.ip_address:
                    print(f"{device.name:<22} {device.ip_address:>15} {device.network_name:<18} {device.activity:>8} Bytes/s {device.uptime:>6} s")
                else:
                    print(f"{device.name:<22} {'--':^15} {device.network_name:<18} {device.activity:>8} Bytes/s {device.uptime:>6} s")
            dump_raw_data(args, device)
    return 0

def arg_parser(subparsers: _SubParsersAction) -> None:
    """Configures arguments parser for 'clients' command"""
    clients_parser = subparsers.add_parser(
        "clients",
        aliases=['c'],
        help="Lists online client devices managed by Omada Controller")
    clients_parser.add_argument('-d', '--dump', help="Output raw device information",  action='store_true')

    clients_parser.set_defaults(func=command_clients)
