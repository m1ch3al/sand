#!/bin/bash

INTERFACE=$1

cat /proc/net/dev | egrep "($INTERFACE|face)" | sed -e 's/|/:/' | sed -e 's/|/ /' | cut -d ":" -f 2 | tr -s " " " "


#cat /proc/net/dev | egrep "($INTERFACE|face)" | sed -e 's/|/:/' | sed -e 's/|/ /' | cut -d ":" -f 2 | tr -s " " " " | \
#awk 'BEGIN {FS=" "} {for (i=1;i<=NF;i++){ arr[NR,i]=$i; if(big <= NF) big=NF; }} \
#END {for(i=1;i<=big;i++){for(j=1;j<=NR;j++){printf("%s:",arr[j,i]);}printf("\n");}}'