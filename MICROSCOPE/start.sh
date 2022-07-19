export DISPLAY=:0
xhost +

sudo pkill fbi
sudo pkill python
sudo pkill vlc

cd ~/MICROSCOPE/src
sudo fbi -T 1 -noverbose -a ~/MICROSCOPE/img/hh/black_screen.jpg &

python3 ~/MICROSCOPE/src/microscope.py -c hh
