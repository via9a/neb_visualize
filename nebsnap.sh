#!/bin/bash

file=$1
start=$2
end=$3

python neb_snapshots.py $file $start $end
