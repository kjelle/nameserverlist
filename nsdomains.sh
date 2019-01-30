#!/bin/bash
cat domains.txt | while read domain ;
do
        [[ $domain = \#* ]] && continue
        domain=$(awk '{ print tolower($0) }' <<< $domain)
        dig +short -t ns $domain | while read line ;
        do
               ip=`dig +short -t a $line`;
               fqdn=$(sed 's/\.$//' <<< $line)              
               echo "{\"fqdn\":\"$fqdn\",\"ip\":\"$ip\",\"ns\":\"domain\",\"domain\":\"$domain\"}"
        done
done

