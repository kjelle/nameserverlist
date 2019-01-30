#!/bin/bash

curl -s http://data.iana.org/TLD/tlds-alpha-by-domain.txt -o tlds-alpha-by-domain.txt

cat tlds-alpha-by-domain.txt | while read tld ;
do
        [[ $tld = \#* ]] && continue

        tld=$(awk '{ print tolower($0) }' <<< $tld)
        dig +short -t ns $tld | while read line ;
        do
               dig +short -t a $line | while read ip ;
               do 
                   fqdn=$(sed 's/\.$//' <<< $line)              
                   echo "{\"fqdn\":\"$fqdn\",\"ip\":\"$ip\",\"ns\":\"tld\",\"tld\":\"$tld\"}"
               done
        done
done

