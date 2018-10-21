#!/bin/bash
. ./bin/activate
env AA_GEOS5_SKIP_LOAD=True python ./test.py
sort cyprus_input.csv |  python ./source_to_train_data.py > cyprus_train_model.csv
python ./trainer.py
