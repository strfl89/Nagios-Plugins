#########################################################################################
#
# Desc: Nagios Script for checking time diff between internal and external NTP Server
#
# Date: Jan 17 2018
# Auth: F.Strunk (strfl89 [at] my-uc-lab.de)
#
#########################################################################################
#
# !!! BROKEN DRAFT / DEVELOPMENT VERSION !!!
#
#########################################################################################

import sys
import getopt
import socket
import struct, time
from socket import AF_INET, SOCK_DGRAM


def getNTPTime(host):
        port = 123
        buf = 1024
        address = (host,port)
        msg = '\x1b' + 47 * '\0'

        # reference time (in seconds since 1900-01-01 00:00:00)
        TIME1970 = 2208988800L # 1970-01-01 00:00:00

        # connect to server
        client = socket.socket( AF_INET, SOCK_DGRAM)
        client.sendto(msg, address)
        msg, address = client.recvfrom( buf )

        t = struct.unpack( "!12I", msg )[10]
        t -= TIME1970
        return time.ctime(t).replace("  "," ")
		
def main(argv):
   internal = ''
   external = ''
   warn = ''
   crit = ''
   try:
      opts, args = getopt.getopt(argv,"hi:e:w:c:",["internal=","external=","warn=","crit="])
   except getopt.GetoptError:
      print 'test.py -i <internal ntp> -e <external ntp> -w <warn msec> -c <crit msec>'
      sys.exit(3)
   for opt, arg in opts:
      if opt == '-h':
         print 'test.py -i <internal ntp> -e <external ntp> -w <warn msec> -c <crit msec>'
         sys.exit()
      elif opt in ("-i", "--internal"):
         internal = arg
      elif opt in ("-e", "--external"):
         external = arg
      elif opt in ("-w", "--warn"):
         warn = arg		 
      elif opt in ("-c", "--crit"):
         crit = arg
		 
   time_int = getNTPTime(internal)
   time_ext = getNTPTime(external)
   
   print 'Output file is "', outputfile

if __name__ == "__main__":
   main(sys.argv[2:])		
		
