#!/bin/bash

version=$1
python -u predict.py --root_path=model_$version --batch_size=1 --use_beam_search=True
