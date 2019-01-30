#!/bin/bash
cat public_dns.txt | while read line ;
do
        [[ $line = \#* ]] && continue
        [ -z $line ] && continue
        line=$(awk '{ print tolower($0) }' <<< $line)
        fqdn=$(cut -d, -f1 <<< $line)
        tags=$(cut -d, -f2- <<< $line)

        dig +short -t a $fqdn | grep '^[.0-9]*$' | while read ip ;
        do            
            if [[ $fqdn =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
                fqdn=""
            fi
            echo "{\"fqdn\":\"$fqdn\",\"ip\":\"$ip\",\"ns\":\"public\",\"tags\":\"$tags\"}"
        done
done

