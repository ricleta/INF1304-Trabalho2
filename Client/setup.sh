#!/bin/bash

# Check if virtual environment directory exists
if [ ! -d "venv" ]; then
    # Check if virtualenv is installed
    if ! command -v python3 -m venv &> /dev/null; then
        echo "Python3 virtual environment is not installed."
        echo "Please install virtualenv by running \"pip install virtualenv\"."
        exit 1
    fi

    echo "Creating virtual environment..."
    # Create virtual environment
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install required packages
echo "Installing required packages..."
pip install -r requirements.txt

echo "Setup complete!"
echo "To run the client, run \"python3 interface.py\"."
echo "To deactivate the virtual environment, run \"deactivate\"."