#!/bin/bash

python docToTxt.py
python convoParser.py
python convBySpeakerParser.py
cd ../data/trainData
cat conv*@* > train_speakers.txt
shopt -s extglob
cat !(*@*|*.txt) > train_origin.txt
