"""Implementation for 'client' command"""

from argparse import ArgumentParser

from .config import get_target_config, to_omada_connection
from .util import dump_raw_data, get_mac, get_target_argument

async def command_client(args) -> int:
    """Executes 'client' command"""
    controller = get_target_argument(args)
    config = get_target_config(controller)

    async with to_omada_connection(config) as client:
        site_client = await client.get_site_client(config.site)
        client_device = await site_client.get_client_device(args['mac'])
        print(f"Name: {client_device.name}")
        print(f"Address: {client_device.mac} ({client_device.ip_address})")
        print(f"Connected: {client_device.active} ")
        print(f"Uptime: {client_device.uptime} s")
        print(f"Last Seen: {client_device.last_seen}")

        dump_raw_data(args, client_device)

    return 0

def arg_parser(subparsers) -> None:
    """Configures arguments parser for 'client' command"""
    client_parser: ArgumentParser = subparsers.add_parser(
        "client",
        help="Shows details about the specified client device"
    )
    client_parser.set_defaults(func=command_client)

    client_parser.add_argument(
        "mac",
        help="The MAC address of the client device",
    )

    client_parser.add_argument('-d', '--dump', help="Output raw device information",  action='store_true')