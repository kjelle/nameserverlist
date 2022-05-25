#!/bin/python3

from urllib.request import urlopen, Request
import urllib
import ssl
import sys
import re


def request(url):
    web_request = Request(
        url,
        data=None,
        headers={}
    )

    try:
        with urlopen(web_request, context=ssl.create_default_context()) as response:
            if response.status != 200:
                return None
            else:
                return response.read().decode('utf-8')
    except urllib.error.HTTPError:
        return None


def ns_root():
    root_data = request("https://www.internic.net/domain/named.root")
    if root_data is None:
        return None
    else:
        root_servers = []
        for line in root_data.split('\n'):
            if " A " in line:
                fqdn_regex = r"^[A-Z]\.[A-Z-]{1,}\.(NET)"
                ip_regex = r"(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$"
                fqdn = re.search(fqdn_regex, line, re.MULTILINE).group()
                ip = re.search(ip_regex, line, re.MULTILINE).group()
                json_object = {
                    "fqdn": fqdn,
                    "ip": ip,
                    "ns": "root"
                }
                root_servers.append(json_object)

        return root_servers


if __name__ == "__main__":
    ns_root()
