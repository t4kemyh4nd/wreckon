#!/bin/bash
#recon script by takemyhand and YashitM

if [ $# -eq 0 ] || [ $# -eq 1 ];
 then
    echo "Usage: ./wreckon.sh sdbf/sdd/dbf/nikto/niktossl domain"
    exit 1
fi

result_file="/tmp/result.txt"

method=$1
domain=$2

dirsearch_scan () {
	x=`date +%s`
	python3 ~/Pentesting/dirsearch/dirsearch.py -b -u $1 -w test.txt -e * --plain-text-report=$x.txt > /dev/null
	cat $x.txt
	rm $x.txt
	exit 0
}

knock_scan () {
	echo "brute-forcing $1 subdomains now"
	python ~/Pentesting/knock/knockpy/knockpy.py -w ~/Pentesting/knock/knockpy/wordlist/wordlist.txt -c $1 > /dev/null
	cat *.csv | cut -d "," -f 4
	rm *.csv
}

aquatone_scan () {
	echo "using aquatone-discover on $1 now"
	aquatone-discover --domain $1 > /dev/null
	cat ~/aquatone/$1/hosts.txt | cut -d "," -f 1
}

nikto_scan () {
	x=`date +%s`
	nikto -host $1 > $x.txt
	cat $x.txt
	rm $x.txt
}

niktossl_scan () {
	x=`date +%s`
	nikto -host $1 -ssl > $x.txt
	cat $x.txt
	rm $x.txt
}

case $method in
"sdbf")
knock_scan $domain
;;
"sdd")
aquatone_scan $domain
;;
"dbf")
dirsearch_scan $domain
;;
"nikto")
nikto_scan $domain
;;
"niktossl")
niktossl_scan $domain
;;
*)
echo "please enter either sdbf or sdd as argument"
;;
esac


#todo- add virustotal API key in knock config.json
#use functions
