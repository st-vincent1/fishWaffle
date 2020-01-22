#!/bin/bash
python train_waffler.py origin 2>&1 | tee -a /home/acq19sk/originerr.txt
python train_waffler.py speakers 2>&1 | tee -a /home/acq19sk/speakerserr.txt
