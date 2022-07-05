export DISPLAY=:0
xhost +

sudo pkill python
sudo pkill vlc

cd ~/MICROSCOPE/src

python3 ~/MICROSCOPE/src/microscope.py -c hh
