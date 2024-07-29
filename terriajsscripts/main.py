from argparse import ArgumentParser, RawDescriptionHelpFormatter

from .decode_sharedata import decode_sharedata
from .encode_sharedata import encode_sharedata


p = ArgumentParser(prog="tjs")
p_sub = p.add_subparsers(metavar="<command>", required=True)
p_share = p_sub.add_parser(
    "share",
    help="Working with share data or shara URLs.",
)
p_share_sub = p_share.add_subparsers(metavar="<subcommand>", required=True)
p_share_decode = p_share_sub.add_parser(
    "decode",
    help="Decodes a share URL into JSON.",
    description="Decodes a share URL into JSON. Reads from stdin and writes to stdout. \n\n"
    "example:\n"
    "  $ echo https://pss-terria.com/#share=s-RBfZnezRe4XWXspi | tjs share decode\n"
    '  {"initSources": {...}}',
    formatter_class=RawDescriptionHelpFormatter,
)
p_share_decode.set_defaults(func=lambda _: decode_sharedata())
p_share_encode = p_share_sub.add_parser(
    "encode",
    help="Encodes a catalog item/init source/share data into a URL.",
    description="Encodes a catalog item/init source/share data into a URL. "
    "Reads from stdin and writes to stdout.\n\n"
    "example:\n"
    "  $ cat item.json\n"
    '  {"type": "3d-tiles", "name": "test", "url": "https://example.com/tileset.json"}\n'
    "  $ cat item.json | tjs share encode --base-url=https://pss-terria.com\n"
    "  https://pss-terria.com#start=%7B%22initSources%22%3A%5B%7B%22stratum%22%3A%...",
    formatter_class=RawDescriptionHelpFormatter,
)
p_share_encode.add_argument(
    "--base-url",
    help="The URL onto which to attach the share fragment. e.g. https://pss-terria.com",
)
p_share_encode.set_defaults(func=lambda args: encode_sharedata(base_url=args.base_url))


if __name__ == "__main__":
    args = p.parse_args()
    args.func(args)
