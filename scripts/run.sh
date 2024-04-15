#!/bin/bash

tmux new -s webserver -d
tmux send-keys 'python server.py' C-m