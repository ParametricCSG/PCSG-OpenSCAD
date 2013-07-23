#! /bin/bash
SCRIPT_PATH="`dirname \"$0\"`"              # relative
SCIPT_PATH="`( cd \"$MY_PATH\" && pwd )`"  # absolutized and normalized

echo "Installing Python modules..."
python3.3 $SCRIPT_PATH/setup.py install

echo "Running tests"
cd tests
python3.3 -m unittest -v
cd ..

echo "Installing textcad in /usr/local/bin/"
cp $SCRIPT_PATH/textcad_engine.py /usr/local/bin/textcad
chmod +x /usr/local/bin/textcad

echo "Finished!"

