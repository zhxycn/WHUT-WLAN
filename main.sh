#!/bin/bash

while getopts "u:p:" opt; do
    case $opt in
        u) USERNAME="$OPTARG" ;;
        p) PASSWORD="$OPTARG" ;;
        *) ;;
    esac
done

SESSION=$(mktemp)

LOGIN_URL=$(curl -Ls -c "$SESSION" -b "$SESSION" -o /dev/null -w "%{url_effective}" "http://www.msftconnecttest.com/redirect")
NASID=$(echo "$LOGIN_URL" | grep -oP 'nasId=\K[^&]+')

CSRF_TOKEN=$(curl -s -c "$SESSION" -b "$SESSION" "http://172.30.21.100/api/csrf-token" | grep -oP '"csrf_token"\s*:\s*"\K[^"]+')

RESPONSE=$(curl -s -X POST "http://172.30.21.100/api/account/login" \
    -c "$SESSION" -b "$SESSION" \
    -H "content-type: application/x-www-form-urlencoded" \
    -H "x-csrf-token: $CSRF_TOKEN" \
    --data "username=$USERNAME&password=$PASSWORD&switchip=&nasId=$NASID&userIpv4=&userMac=&captcha=&captchaId=")

echo "$RESPONSE"

rm -f "$SESSION"
