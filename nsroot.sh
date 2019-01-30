#!/bin/bash

curl -s http://www.internic.net/domain/named.root -o named.root

grep " A " named.root | while read line ; 
do
        fqdn=$(awk '{ print tolower($1) }' <<< $line | sed 's/\.$//')
        ip=$(awk '{ print $4 }' <<< $line)
        echo "{\"fqdn\":\"$fqdn\",\"ip\":\"$ip\",\"ns\":\"root\"}"
done

