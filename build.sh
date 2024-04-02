#!/bin/bash

# Update pip
echo "Updating pip..."
python3.9 pip install -U pip

# Install dependencies

echo "Installing project dependencies..."
python3.9 -m pip install -r requirements.txt