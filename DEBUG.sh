#!/bin/sh
################################################################################
# file: /root/DEBUG/milano/DEBUG.sh
# auth: andreoidb64
# date: 20160429
#
#
################################################################################

case $1 in
-start) cd /root/DEBUG/milano
	while sleep 2; do sync; done &
	./run.sh
	exit
	;;
 -stop) killall python2.5
	killall msd
	killall fbserver
	exit
	;;
     *) ;;
esac

### Edit your project and remove ".PYC" compiled before run Webby in debug env.
# vi /root/DEBUG/milano/launcher/manager/netmgr.py
# rm /root/DEBUG/milano/launcher/manager/netmgr.pyc

### Remove logs before run Webby in debug environment (if needed)
# rm /root/user_data/log/*

$0 -stop
sleep 2
nohup $0 -start 1>/root/user_data/log/WebbyDebugMode.log 2>&1 &
