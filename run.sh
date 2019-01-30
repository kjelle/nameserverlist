#!/bin/bash

echo "fetching root"
bash nsroot.sh > nameservers.json

echo "fetching tld"
bash nstld.sh >> nameservers.json

echo "fetching domains (sld)"
bash nsdomains.sh >> nameservers.json

echo "building public DNS"
bash public_dns.sh >> nameservers.json
