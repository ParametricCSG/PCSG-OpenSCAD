#! /bin/bash
SCRIPT_PATH="`dirname \"$0\"`"              # relative
SCIPT_PATH="`( cd \"$MY_PATH\" && pwd )`"  # absolutized and normalized

echo "Installing Python modules..."
python3.3 $SCRIPT_PATH/setup.py install

echo "Installing pcsg-openscad"
cp $SCRIPT_PATH/textcad_engine.py /usr/local/bin/textcad
chmod +x /usr/local/bin/textcad

echo "Finished!"
