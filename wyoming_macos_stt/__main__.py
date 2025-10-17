#!/usr/bin/env python3
import argparse
import asyncio
import logging
import os
from functools import partial
from logging.handlers import TimedRotatingFileHandler

from wyoming.server import AsyncServer

from . import __version__
from .handler import MacosSTTEventHandler

_LOGGER = logging.getLogger("wyoming-macos-stt")


async def main() -> None:
    """Main entry point."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--uri", required=True, help="unix:// or tcp://")
    parser.add_argument(
        "--service-name",
        default="macos-stt",
        help="Name that will be sent in the info event",
    )
    parser.add_argument(
        "--yap-args",
        default="",
        help="Arguments to pass to the yap CLI tool (see: yap --help)",
    )
    parser.add_argument("--debug", action="store_true", help="Log DEBUG messages")
    parser.add_argument(
        "--log-format",
        default="%(asctime)s [%(levelname)s] %(message)s",
        help="Format for log messages",
    )
    parser.add_argument(
        "--log-dir",
        help="Directory to store the logs (leave empty to not save any logs)",
    )
    parser.add_argument(
        "--log-keep-days", default=7, help="Number of days to keep logs"
    )
    parser.add_argument(
        "--version",
        action="version",
        version=__version__,
        help="Print version and exit",
    )
    args = parser.parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.debug else logging.INFO, format=args.log_format
    )
    if args.log_dir:
        os.makedirs(args.log_dir, exist_ok=True)
        handler = TimedRotatingFileHandler(
            os.path.join(args.log_dir, "app.log"),
            when="midnight",
            backupCount=int(args.log_keep_days),
        )
        handler.setFormatter(logging.Formatter(args.log_format))
        _LOGGER.addHandler(handler)
    _LOGGER.debug(f"Starting server with args: {args}")

    server = AsyncServer.from_uri(args.uri)
    _LOGGER.info("Ready")

    await server.run(partial(MacosSTTEventHandler, args))


def run() -> None:
    asyncio.run(main())


if __name__ == "__main__":
    try:
        run()
    except KeyboardInterrupt:
        pass
