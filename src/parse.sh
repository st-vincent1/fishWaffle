#!/bin/bash

python docToTxt.py
python convoParser.py
cd ../data/trainData
cat * > train.txt
