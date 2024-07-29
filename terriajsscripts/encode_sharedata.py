from sys import stdin, stdout
from typing import Any
from urllib.parse import urldefrag, urlencode, parse_qs
from uuid import uuid4
import json


def encode_sharedata(*, base_url: str):
    obj: dict[Any, Any] = json.load(stdin)
    base = base_url or obj.pop("__BASE_URL", "")

    url, fragment = urldefrag(base)
    params = parse_qs(fragment)

    if "type" in obj:
        # Looks like obj is a bare catalog item. Wrap it into a complete init source.

        # Change id across runs so that Terria creates a new catalog item
        # rather than updating a previously-loaded one.
        obj = {**obj, "id": str(uuid4())}
        obj = {"stratum": "user", "catalog": [obj], "workbench": [obj["id"]]}

    if "initSources" not in obj:
        # Looks like obj is a bare init source. Wrap it into a complete share data.
        obj = {"initSources": [obj]}

    json_string = json.dumps(obj, ensure_ascii=False, separators=(",", ":"))

    params["start"] = [json_string]
    stdout.write("".join([url, "#", urlencode(params, doseq=True)]))
