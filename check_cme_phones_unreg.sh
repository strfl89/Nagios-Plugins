#!/bin/bash


while getopts 'H:C:w:c:' OPTION ; do
  case "$OPTION" in
    H)   HOST=$OPTARG;;
    C)   COMMUNITY=$OPTARG;;
    w)   warn=$OPTARG;;
    c)   crit=$OPTARG;;
  esac
done


TOT=`/usr/bin/snmpwalk $HOST -v 2c -c $COMMUNITY -Ovq iso.3.6.1.4.1.9.9.439.1.2.2.0`

REG=`/usr/bin/snmpwalk $HOST -v 2c -c $COMMUNITY -Ovq iso.3.6.1.4.1.9.9.439.1.2.3.0`

UNREG=$(echo "$TOT - $REG" | bc)

output="$UNREG Unregisterd Phone(s)"

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
