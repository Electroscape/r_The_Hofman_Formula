import argparse
import board
import busio
import json
import os
import vlc



from adafruit_pn532.adafruit_pn532 import MIFARE_CMD_AUTH_A
from adafruit_pn532.i2c import PN532_I2C
from time import sleep
'''
=========================================================================================================
Argument parser
=========================================================================================================
'''
argparser = argparse.ArgumentParser(
    description='Microscope')

argparser.add_argument(
    '-c',
    '--city',
    help='name of the city: [hh / st]')

city = argparser.parse_args().city

'''
=========================================================================================================
Load config
=========================================================================================================
'''
with open('config.json', 'r') as config_file:
    config = json.load(config_file)


'''
=========================================================================================================
PN532 init
=========================================================================================================
'''

# I2C connection:
i2c = busio.I2C(board.SCL, board.SDA)

pn532 = PN532_I2C(i2c, debug=False)
ic, ver, rev, support = pn532.firmware_version
print("Found PN532 with firmware version: {0}.{1}".format(ver, rev))
pn532.SAM_configuration() # Configure PN532 to communicate with MiFare cards


'''
=========================================================================================================
Global VLC variables
=========================================================================================================
'''

vlc_instance = vlc.Instance( ) # creating Instance class object
player = vlc_instance.media_player_new() # creating a new media object


'''
=========================================================================================================
VLC init
=========================================================================================================
'''

def play_video(path):

    '''
    Description
    -----------
    Displaying the video once sensor is high
    set the mrl of the video to the mediaplayer
    play the video and

    

    '''
    player.set_fullscreen(True) # set full screen
    player.set_mrl(path)    #setting the media in the mediaplayer object created
    player.play()           # play the video
    

'''
=========================================================================================================
RFID functions
=========================================================================================================
'''

def rfid_read(uid, block):

    '''
    Checks if the card is read or not 
    '''

    try:
        # if classic tag
        auth = authenticate(uid, block)
    except Exception:
        # if ntag
        auth = False

    try:
        # Switch between ntag and classic
        if auth:  # True for classic and False for ntags
            data = pn532.mifare_classic_read_block(block)
        else:
            data = pn532.ntag2xx_read_block(block)

        if data is not None:
            read_data = data.decode('utf-8')[:2]
            
        else:
            read_data = False
            print("None block")

    except Exception as e:
        print(e)

    return read_data

def rfid_present():

    '''
    checks if the card is present inside the box
    '''
    try:
        uid = pn532.read_passive_target(timeout=0.5) #read the card
    except RuntimeError:
        uid = None
        return uid 
    return uid


def authenticate(uid, read_block):
    rc = 0
    key = [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF]
    rc = pn532.mifare_classic_authenticate_block(
        uid, config["BLOCK"]["read_block"], MIFARE_CMD_AUTH_A, key)
    print(rc)
    return rc

'''
=========================================================================================================
"MAIN"
=========================================================================================================
'''

def main():
    ptoe = False    #Periodic table of elements

    while True:
        
        if rfid_present():
            if rfid_read(rfid_present(),config["BLOCK"]["read_block"]) == "VR":
                ptoe = False
                play_video(config['PATH']['image']  + city +  "/Screen1.png")
            else:
                print('Wrong Card')
            
            while rfid_present():
                continue
        else:
            if ptoe == False:
                
                ptoe = True
                play_video(config['PATH']['video'] + "/Periodensystem_169_schwarz.mp4")
               
            else:
                if player.get_state() == vlc.State.Ended :
                    ptoe = False
                      

if __name__ == "__main__":
    main()

