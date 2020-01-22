#!/bin/bash
conda activate fishEnv
python modeling.py origin 2>&1 | tee -a originerr.txt
python modeling.py speakers 2>&1 | tee -a speakerserr.txt
