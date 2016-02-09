#!/bin/bash

# initialization of variables
HOST="127.0.0.1"
COMMUNITY="public"
warn=10
crit=25
output=""


#get Options and save Option Arguments to variables
while getopts 'H:C:w:c:' OPTION ; do
  case "$OPTION" in
    H)   HOST=$OPTARG;;
    C)   COMMUNITY=$OPTARG;;
    w)   warn=$OPTARG;;
    c)   crit=$OPTARG;;
  esac
done


#get total phones & registerd phones via SNMP
TOT=`/usr/bin/snmpwalk $HOST -v 2c -c $COMMUNITY -Ovq iso.3.6.1.4.1.9.9.439.1.2.2.0`

REG=`/usr/bin/snmpwalk $HOST -v 2c -c $COMMUNITY -Ovq iso.3.6.1.4.1.9.9.439.1.2.3.0`

UNREG=$(echo "$TOT - $REG" | bc)

output="$UNREG Unregisterd Phone(s)"


# check unregistertd phones with warn / crit and generate Nagios output
if [ "$UNREG" -ge "$crit" ]
  then
	echo "CRITICAL - $output"
	exit 2
  elif [ "$UNREG" -ge "$warn" ]
	then
	    echo "WARNING - $output"
	    exit 1
	elif [ "$UNREG" -lt "$warn" ]
	    then
		echo "OK - $output"
		exit 0
else
echo "UNKNOWN - $output"
exit 3
fi
