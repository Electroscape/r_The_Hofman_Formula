# Microscope
# for clean start, kill all relevenat programs
sudo pkill python
sudo pkill fbi
sudo pkill vlc

cd ~/MICROSCOPE
# for smooth transition instead of terminal appearance
sudo fbi -a -T 1 --noverbose img/blackscreen.jpg &
python src/microscope.py
