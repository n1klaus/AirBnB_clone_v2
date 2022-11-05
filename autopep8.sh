#!/usr/bin/env bash
# Fix python scripts styling with autopep8 guidelines and pycodestyle style guide
VENV='./start/*'
if [ "$(/usr/bin/which autopep8 | wc -l)" == 0 ]
then
    echo "missing package, start installing autopep8..."
    sudo apt-get update -y > /dev/null 2>&1 &&\
	sudo apt-get install autopep8 -y > /dev/null 2>&1
fi

echo "Running autopep..."
find . -type f -name '*.py' ! -path '*/migrations/*' ! -path "$VENV" -exec \
    autopep8 --in-place --aggressive --recursive --verbose '{}' \;

if [ "$(/usr/bin/which pycodestyle | wc -l)" == 0 ]
then
    echo "missing package, start installing pycodestyle..."
    sudo apt-get update -y > /dev/null 2>&1 &&\
	sudo apt-get install autopep8 -y > /dev/null 2>&1
fi

echo -e "\n\nRunning pycodestyle..."
find . -type f -name '*.py' ! -path '*/migrations/*' ! -path "$VENV" -exec pycodestyle --verbose '{}' \;

echo -e "\nDone"