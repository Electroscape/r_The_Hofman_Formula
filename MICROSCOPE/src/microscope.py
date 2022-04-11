from time import sleep
import os

import board
import busio

from adafruit_pn532.i2c import PN532_I2C
from adafruit_pn532.adafruit_pn532 import MIFARE_CMD_AUTH_A


# First of all, Play the periodic system
pic_path = 'Screen1.png'
vid_path = 'Periodensystem_169_schwarz.mp4' 
cmnd = 'cvlc {0} -f --no-osd --loop &'
vid_command = cmnd.format(f"vid/{vid_path}")
pic_command = cmnd.format(f"img/{pic_path}")

# clean start
# Kill all relavent applications
os.system("sudo pkill vlc")
# run video
os.system(vid_command)

# I2C connection:
i2c = busio.I2C(board.SCL, board.SDA)
read_block = 1

# keep trying to initialise the sensor
while True:
    try:
        # Non-hardware reset/request with I2C
        pn532 = PN532_I2C(i2c, debug=False)
        ic, ver, rev, support = pn532.firmware_version
        print("Found PN532 with firmware version: {0}.{1}".format(ver, rev))
        break
    except:
        print("failed to start RFID")
        sleep(1)

# this delay avoids some problems after wakeup
sleep(1)

# Configure PN532 to communicate with MiFare cards
pn532.SAM_configuration()


def wait_remove_card(uid):
    while uid:
        # print('Same Card Still there')
        # sleep(0.01)
        try:
            uid = pn532.read_passive_target()
        except RuntimeError:
            uid = None


def scan_field():
    while True:
        try:
            uid = pn532.read_passive_target()
        except (RuntimeError, BusyError):
            uid = None
            # sleep(0.01)

        # print('.', end="") if count <= 3 else print("", end="\r")
        # Try again if no card is available.
        if uid:
            print('Found card')
            break

    return uid

def authenticate(uid, read_block):
    rc = 0
    key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
    rc = pn532.mifare_classic_authenticate_block(
        uid, read_block, MIFARE_CMD_AUTH_A, key)
    print(rc)
    return rc

def main():

    print('Welcome to Microscope')
    print('Waiting Card')

    while True:
        uid = scan_field()

        if uid:
            print('Card found')
            try:
                # if classic tag
                auth = authenticate(uid, read_block)
            except Exception:
                # if ntag
                auth = False

            try:
                # Switch between ntag and classic
                if auth:  # True for classic and False for ntags
                    data = pn532.mifare_classic_read_block(read_block)
                else:
                    data = pn532.ntag2xx_read_block(read_block)

                if data is not None:
                    read_data = data.decode('utf-8')[:2]
                else:
                    print("None block")
            except Exception as e:
                print(e)

            print('data is: {}'.format(read_data))
            
            success = False
            if read_data == "VR": 
                os.system("sudo pkill vlc")
                os.system(pic_command)
                print('Virus detected')
                success = True
            else:
                success = False
                print('Wrong Card')
            
            wait_remove_card(uid)

            print("Card Removed")
            if success:
                os.system("sudo pkill vlc")
                os.system(vid_command)

if __name__ == "__main__":
    main()

