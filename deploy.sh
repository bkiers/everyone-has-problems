#!/usr/bin/env bash

read -p "Sync local .mp3 and .png files with Firebase Storage? [Yn]: " answer

if [[ "$answer" = "" ]] || [[ "$answer" = "y" ]] || [[ "$answer" = "Y" ]]; then
    cd ./generator
    source env/bin/activate
    python main.py
    cd ..
else
    echo "Skipping sync with Firebase Storage"
fi

firebase deploy

echo ""
echo "Done!"
