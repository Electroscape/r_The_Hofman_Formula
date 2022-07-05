export DISPLAY=:0
xhost +

sudo pkill python
sudo pkill vlc

cd ~/MICROSCOPE

python3 src/microscope.py -c hh
