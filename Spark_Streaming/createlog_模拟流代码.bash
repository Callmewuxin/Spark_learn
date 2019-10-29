#! bin/bash
# HDFS命令
HDFS="/usr/local/hadoop/bin/hadoop fs"
# Streaming 监听的文件目录
streaming_dir="/user/hadoop/streaming/information"

# 生成日志
cat Information.json | while read line
do
		rm -rf ~/Downloads/information/log/*
        tmplog="~/Downloads/information/log/`date +'%s'`.log"
        echo $line>$tmplog
        $HDFS -put $tmplog $streaming_dir
done