#!/bin/bash

> parameters.txt
echo $1.>> parameters.txt

python model_deploy.py
