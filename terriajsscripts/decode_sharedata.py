from base64 import b64encode
import re
from sys import stdin, stdout
from typing import Optional
from urllib.request import Request, urlopen
from urllib.parse import unquote_plus, urljoin
import json


def decode_sharedata(username: Optional[str] = None, password: Optional[str] = None):
    long_url = stdin.read()
    DELIMITER = "#start="

    if m := re.search(r"(.+)(#start=)(.+)", long_url):
        prefix = m[1]
        encoded_data = m[3]
        decoded_data = json.loads(unquote_plus(encoded_data))
    elif m := re.search(r"(.+)(#share=)(.+)", long_url):
        prefix = m[1]
        share_key = m[3]
        share_data_url = urljoin(long_url, f"/share/{share_key}")
        headers: dict[str, str] = {}
        if username and password:
            headers["Authorization"] = "Basic " + (
                b64encode(f"{username}:{password}".encode("utf8")).decode("utf8")
            )
        elif not username and not password:
            # No auth
            pass
        else:
            assert (
                False
            ), "You have to provide both username and password if you want to access an auth-protected terriajs app."
        request = Request(share_data_url, headers=headers)
        with urlopen(request) as rs:
            decoded_data = json.load(rs)
    else:
        raise Exception("URL malformatted.")

    decoded_data = {"__BASE_URL": f"{prefix}{DELIMITER}", **decoded_data}
    json.dump(decoded_data, stdout, indent=2, ensure_ascii=False)
