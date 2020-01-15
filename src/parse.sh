#!/bin/bash

python docToTxt.py
python convoParser.py
cd ../data/trainData
cat * > tmp
rm -f train.txt
mv tmp train.txt
