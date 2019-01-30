#!/bin/bash

echo "fetching root"
bash nsroot.sh > json/nsroot.json

echo "fetching tld"
bash nstld.sh > json/nstld.json

echo "fetching domains (sld)"
bash nsdomains.sh > json/nsdomains.json

echo "building public DNS"
bash public_dns.sh > json/public_dns.json
