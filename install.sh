#! /bin/bash
echo "Installing Python modules..."
python3.3 setup.py install

echo "Installing pcsg-openscad"
cp ./pcsg_openscad.py /usr/local/bin/pcsg-openscad
chmod +x /usr/local/bin/pcsg-openscad

echo "Finished!"
