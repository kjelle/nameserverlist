#!/bin/python3

from urllib.request import urlopen, Request
from json import dump
import dns.resolver
import logging
import urllib
import ssl
import sys
import re

logging.basicConfig(level=logging.INFO)
logging.getLogger().setLevel(logging.INFO)


def writejson(file, data):
    with open(file, 'w') as f:
        dump(data, f)

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


def dig_tld(tld):
    ip_regex = r"(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])"
    tld_data = []
    try:
        for rdata in dns.resolver.resolve(tld, 'ns'):
            data = str(rdata).split('\n')
            for entry in data:
                dns_query = str(dns.resolver.resolve(entry, 'A').response)
                entry_ip = re.search(ip_regex, dns_query, re.MULTILINE).group()

                # replace the last dot e.g. "ns1.dns.nic.aaa." to "ns1.dns.nic.aaa"
                entry = entry[::-1].replace(".", "", 1)
                entry = entry[::-1]
                tld_data.append({
                    "fqdn": entry,
                    "ip": entry_ip,
                    "ns": "tld",
                    "tld": tld
                })
    except dns.resolver.NoNameservers:
        logging.error(f"Error while fetching tld: {tld}")
        return []
    except dns.resolver.NoAnswer:
        logging.error(f"Error while fetching tld: {tld}")
        return []
    except dns.resolver.LifetimeTimeout:
        logging.error(f"Error while fetching tld: {tld}")
        return []
    except dns.resolver.NXDOMAIN:
        logging.error(f"Error while fetching tld: {tld}")
        return []

    return tld_data


def ns_tld():
    tld_data = request("https://data.iana.org/TLD/tlds-alpha-by-domain.txt")
    tlds = []
    if tld_data is None:
        return None
    else:
        for line in tld_data.split('\n'):
            if "#" in line or line == "":
                continue
            logging.info(f"Fetching tld: {line.lower()}")
            tlds = tlds + dig_tld(line.lower())

    writejson("./json/nstld.json", tlds)


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

        writejson("./json/nsroot.json", root_servers)


if __name__ == "__main__":
    arguments = sys.argv
    try:
        arguments[1]
    except IndexError:
        logging.warning("Please define a action to use: root | tld")
        sys.exit()

    if arguments[1] == "root":
        logging.info("Fetching root servers")
        ns_root()
    elif arguments[1] == "tld":
        logging.info("Fetching tld servers")
        ns_tld()
