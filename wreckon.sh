#!/bin/bash
#recon script by takemyhand and YashitM

if [ $# -eq 0 ] || [ $# -eq 1 ];
 then
    echo "Usage: ./wreckon.sh sdbf/sdd domain"
    exit 1
fi

result_file="/tmp/result.txt"

method=$1
domain=$2

case $method in
"sdbf")
touch $result_file
echo "brute-forcing $domain subdomains now"
;;
"sdd")
touch $result_file
echo "using aquatone-discover on $domain now"
aquatone-discover --domain $domain
echo ~/aquatone/$domain/hosts.txt | cut -d "," -f 1
;;
*)
echo "please enter either sdbf or sdd as argument"
;;
esac

