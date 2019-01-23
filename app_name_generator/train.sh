#!/bin/bash

version=$1
python -u train.py --root_path=model_$version
