file_name=/tmp/backup-$(date +"%Y-%m-%d_%H_%M_%S").tar.gz
sysupgrade -b $file_name
rclone copy $file_name backup:/openwrt/ # replace with your rclone folder
