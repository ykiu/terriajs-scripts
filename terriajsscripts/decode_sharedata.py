import re
from sys import stdin, stdout
from urllib import request
from urllib.parse import unquote_plus, urljoin
import json


def decode_sharedata():
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
        with request.urlopen(share_data_url) as rs:
            decoded_data = json.load(rs)
    else:
        raise Exception("URL malformatted.")

    decoded_data = {"__BASE_URL": f"{prefix}{DELIMITER}", **decoded_data}
    json.dump(decoded_data, stdout, indent=2, ensure_ascii=False)
