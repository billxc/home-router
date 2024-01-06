file_name=/tmp/backup-$(date +%F).tar.gz
sysupgrade -b $file_name
rclone copy $file_name backup:/openwrt/ # replace with your rclone folder
