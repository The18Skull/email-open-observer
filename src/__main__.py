from typing import Any
from argparse import ArgumentParser

from . import util

parser = ArgumentParser(description="Kana recognition app")
parser.add_argument("--debug", action="store_true", help="Enable debug logging")
subparser = parser.add_subparsers()
web_cli = subparser.add_parser("serve", help="Start web server")
web_cli.add_argument("--host", help="Host address")
web_cli.add_argument("--port", type=int, help="Port number")
web_cli.set_defaults(cmd="serve")
email_cli = subparser.add_parser("send", help="Send infected email")
email_cli.add_argument("--address", required=True, help="Target's email address")
email_cli.set_defaults(cmd="send")


def parse_args() -> dict[str, Any]:
    args = parser.parse_args()
    kwargs = {"debug": True}
    for k, v in vars(args).items():
        if not v:
            continue
        kwargs.setdefault(k, v)
    return kwargs


def start_server(**kwargs: dict[str, Any]) -> None:
    host = kwargs.get("host", "0.0.0.0")
    port = kwargs.get("port", 8000)
    log_level = "debug" if kwargs.get("debug", True) else "info"
    workers = 1 if kwargs.get("debug", True) else 10

    import uvicorn
    uvicorn.run(
        "src.web:app",
        host=host,
        port=port,
        reload=False,
        log_level=log_level,
        workers=workers,
    )


def send_email(**kwargs: dict[str, Any]) -> None:
    address = kwargs.get("address")

    from .send import send_email
    send_email(address)


if __name__ == "__main__":
    util.create_db()
    kwargs = parse_args()

    command = kwargs.pop("cmd", None)
    if command == "serve":
        start_server(**kwargs)
    elif command == "send":
        send_email(**kwargs)
    else:
        parser.print_help()
