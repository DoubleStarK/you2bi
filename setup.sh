#!/bin/bash
platform=$(uname | tr '[:upper:]' '[:lower:]')
arc=$(uname -m)
if [ "${arc}" == "x86_64" ]; then
    arc="amd64"
elif [ "${arc}" == "arm64" ]; then
    arc="arm64"
fi

if [ -x "./lib/biliup_darwin_amd64" ] && [ -x "./lib/biliup_darwin_amd64" ]; then
    cp "./lib/biliup_${platform}_${arc}" ./biliup
else
    echo "不支持的系统" && exit 1
fi

if [ -r "./cookie.json" ]; then
    echo "您已经登录"
    exit 0
else
    echo "未登录,请登录:"
    ./biliup login
fi
