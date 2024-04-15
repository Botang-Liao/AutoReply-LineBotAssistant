#!/bin/bash
env=flask_server

conda create -y -n $env python=3.9
conda activate $env
pip install -r requirements.txt