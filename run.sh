#!/bin/bash

numbers=(1 4 5 6 8 9 10 11 12 13 15)

for number in "${numbers[@]}"; do
    python my.py $number &
    sleep 7
done

wait
