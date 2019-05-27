#!/bin/bash
#recon script by takemyhand and YashitM

if [ $# -eq 0 ] || [ $# -eq 1 ];
 then
    echo "Usage: ./wreckon.sh sdbf/sdd/dbf domain"
    exit 1
fi

result_file="/tmp/result.txt"

method=$1
domain=$2

case $method in
"sdbf")
touch $result_file
echo "brute-forcing $domain subdomains now"
python ~/Pentesting/knock/knockpy/knockpy.py -w ~/Pentesting/knock/knockpy/wordlist/wordlist.txt -c $domain > /dev/null
cat *.csv | cut -d "," -f 4
rm *.csv
;;
"sdd")
touch $result_file
echo "using aquatone-discover on $domain now"
aquatone-discover --domain $domain > /dev/null
cat ~/aquatone/$domain/hosts.txt | cut -d "," -f 1
;;
"dbf")
python3 ~/Pentesting/dirsearch/dirsearch.py -b -u $domain -e * --plain-text-report=result.txt > /dev/null
cat result.txt
rm result.txt
;;
*)
echo "please enter either sdbf or sdd as argument"
;;
esac


#todo- add virustotal API key in knock config.json
