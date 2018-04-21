#!/bin/sh
################################################################################
# file: /etc/DynDnsRefresh.sh
# auth: andreoidb64
# date: 20180421
#
# NOTE: Run from cron
#
################################################################################

InetIP=999.999.999.999

InetIP=$(/usr/bin/wget -O - http://ident.me/ 2>/dev/null)
/bin/ping -c 3 $InetIP 1>/dev/null 2>&1 || exit 1

echo "To do: Refresh DNS record: $InetIP"
