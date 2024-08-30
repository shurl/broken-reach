#!/bin/sh

cd $(dirname "$0")
cp /ping.log $(dirname "$0")/ping.log
gzip -f $(dirname "$0")/ping.log
rm  $(dirname "$0")/ping.log
git commit -a -m "Update data (cron)"
git push

