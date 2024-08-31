
#!/bin/bash

# Check if tkinter is already installed
python3 -c "import tkinter" 2>/dev/null
if [ $? -eq 0 ]; then
    echo "tkinter is already installed."
else
    # Install system dependencies
    if [ -x "$(command -v apt-get)" ]; then
        sudo apt install -y python3-tk
    elif [ -x "$(command -v dnf)" ]; then
        sudo dnf install -y python3-tkinter
    elif [ -x "$(command -v pacman)" ]; then
        sudo pacman -Sy tk
    else
        echo "Unsupported package manager. Please install tkinter manually."
        exit 1
    fi
fi

# Install Python dependencies using Poetry
pip install selenium
pip install webdriver-manager
pip install poetry
poetry install