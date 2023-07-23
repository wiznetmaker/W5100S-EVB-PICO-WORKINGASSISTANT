import time as utime
import busio
import board
import usb_cdc
from Arducam import *
from board import *

import board
import busio
import digitalio
import time
import gc
from adafruit_wiznet5k.adafruit_wiznet5k import WIZNET5K
from adafruit_wiznet5k.adafruit_wiznet5k import *
from adafruit_wiznet5k.adafruit_wiznet5k_socket import socket
from adafruit_wiznet5k.adafruit_wiznet5k_socket import *
        
once_number=1024
#once_number=128
mode = 0
prev_mode = mode
start_capture = 0
stop_flag=0
data_in=0
value_command=0
flag_command=0
buffer=bytearray(once_number)

mycam = ArducamClass(OV2640)
mycam.Camera_Detection()
mycam.Spi_Test()
mycam.Camera_Init()
utime.sleep(1)
mycam.clear_fifo_flag()

def read_fifo_burst_socket(cli_sock, length):
    count=0
    #lenght=mycam.read_fifo_length()
    mycam.SPI_CS_LOW()
    mycam.set_fifo_burst()
    while True:
        mycam.spi.readinto(buffer,start=0,end=once_number)
        #usb_cdc.data.write(buffer)
        cli_sock.send(buffer)
        #utime.sleep(0.001)
        count+=once_number
        if count+once_number>length:
            count=length-count
            mycam.spi.readinto(buffer,start=0,end=count)
            #usb_cdc.data.write(buffer)
            cli_sock.send(buffer[0:count])
            mycam.SPI_CS_HIGH()
            mycam.clear_fifo_flag()
            break

    gc.collect()    
    return length   


def w5x00_init():
    ##SPI0
    SPI0_SCK = board.GP18
    SPI0_TX = board.GP19
    SPI0_RX = board.GP16
    SPI0_CSn = board.GP17

    ##reset
    W5x00_RSTn = board.GP20

    print("Wiznet5k (DHCP)")

    # Setup your network configuration below
    # random MAC, later should change this value on your vendor ID
    MY_MAC = (0x00, 0x01, 0x02, 0x03, 0x04, 0x05)
    IP_ADDRESS = (192, 168, 0, 5)
    SUBNET_MASK = (255, 255, 255, 0)
    GATEWAY_ADDRESS = (192, 168, 0, 1)
    DNS_SERVER = (8, 8, 8, 8)

    ethernetRst = digitalio.DigitalInOut(W5x00_RSTn)
    ethernetRst.direction = digitalio.Direction.OUTPUT

    led = digitalio.DigitalInOut(board.GP25)
    led.direction = digitalio.Direction.OUTPUT

    # For Adafruit Ethernet FeatherWing
    cs = digitalio.DigitalInOut(SPI0_CSn)
    spi_bus = busio.SPI(SPI0_SCK, MOSI=SPI0_TX, MISO=SPI0_RX)

    # Reset W5500 first
    ethernetRst.value = False
    time.sleep(1)
    ethernetRst.value = True


    # Initialize ethernet interface without DHCP
    eth = WIZNET5K(spi_bus, cs, is_dhcp=True, mac=MY_MAC)

    # Set network configuration
    #eth.ifconfig = (IP_ADDRESS, SUBNET_MASK, GATEWAY_ADDRESS, DNS_SERVER)

    print("Chip Version:", eth.chip)
    print("MAC Address:", [hex(i) for i in eth.mac_address])
    print("My IP address is:", eth.pretty_ip(eth.ip_address))
    print("Done!")

    return eth, led


def httpServer_init():
    eth, led = w5x00_init()
    set_interface(eth)
    sock = socket()
    return sock


def httpServer_listen(sock):
    sock.bind((None, 80))
    sock.listen()
    
def httpServer_accept(sock):    
    cli_sock, addr = sock.accept()
    while not cli_sock.connect:
        time.sleep(0.01)
    print('Connect')
    #print(conn)
    return cli_sock

def httpServer_read(cli_sock):
    request = cli_sock.recv()
    print(request)
    if len(request) > 0:
        #print(request)
        request = request.decode("utf-8")
        #print('Content = %s' % request)
        reqlines = request.split('\r\n')
        #print(reqlines)
        method = reqlines[0].split(' ')
        print(method)
        print(method[1][1:])

        return True, method[1][1:]
    else:
        time.sleep(0.001)
        return False, b''

def httpServer_response_single(cli_sock):
    print('httpServer_response_single()')
    length = mycam.read_fifo_length()
    print(length)
    cli_sock.send(b'HTTP/1.1 200 OK\n')
    cli_sock.send(b'Connection: close\n')
    cli_sock.send(b"Content-Type: image/jpeg\n")
    cli_sock.send(b"Content-Length: %d\n\n" % length)
    read_fifo_burst_socket(cli_sock, length)
    #eth.socket_write(s, b"\n\n")
    print('response done')


BOUNDARY = b"e8b8c539-047d-4777-a985-fbba6edff11e"

def httpServer_response_stream_init(cli_sock):
    print('httpServer_response_stream_init()')
    cli_sock.send(b'HTTP/1.1 200 OK\n')
    cli_sock.send(b'Content-Type: multipart/x-mixed-replace;boundary=' + BOUNDARY + b'\n\n')

def httpServer_response_stream_burst(cli_sock):
    print('httpServer_response_stream_burst()')
    length = mycam.read_fifo_length()
    print(length)
    cli_sock.send(b"Content-Type: image/jpeg\n")
    cli_sock.send(b"Content-Length: %d\n\n" % length)
    read_fifo_burst_socket(cli_sock, length)
    cli_sock.send(b"\n--" + BOUNDARY + b"\n");


def httpServer_close(cli_sock):
    cli_sock.disconnect()
    time.sleep(0.05)


#########################################################################

mycam.OV2640_set_Light_Mode(Auto)
mycam.OV2640_set_Color_Saturation(Saturation0)
mycam.OV2640_set_Brightness(Brightness0)
mycam.OV2640_set_Contrast(Contrast0)
mycam.OV2640_set_Special_effects(Normal)
mycam.Camera_Init()
mycam.set_bit(ARDUCHIP_TIM,VSYNC_LEVEL_MASK)

mycam.OV2640_set_JPEG_size(OV2640_640x480)
#mycam.OV2640_set_JPEG_size(OV2640_160x120)
mycam.set_format(JPEG)
#mycam.Camera_Init()
mycam.set_bit(ARDUCHIP_TIM,VSYNC_LEVEL_MASK)

sock = httpServer_init()
httpServer_listen(sock)

while True:
    cli_sock = httpServer_accept(sock)

    while True:
        has_cmd, cmd = httpServer_read(cli_sock)

        if has_cmd:
            value_command = cmd
            flag_command=1
        if flag_command==1:
            flag_command=0
            #value=int.from_bytes(value_command,"big") 
            try:
                value = int(value_command)
                #print(value)
            except:
                value = -1
                httpServer_close(cli_sock)
                break
                
            if value==0:
                mycam.OV2640_set_JPEG_size(OV2640_160x120)
            elif value==1:
                mycam.OV2640_set_JPEG_size(OV2640_176x144)
            elif value==2:
                mycam.OV2640_set_JPEG_size(OV2640_320x240)
            elif value==3:
                mycam.OV2640_set_JPEG_size(OV2640_352x288)
            elif value==4:
                mycam.OV2640_set_JPEG_size(OV2640_640x480)
            elif value==5:
                mycam.OV2640_set_JPEG_size(OV2640_800x600)
            elif value==6:
                mycam.OV2640_set_JPEG_size(OV2640_1024x768)
            elif value==7:
                mycam.OV2640_set_JPEG_size(OV2640_1280x1024)
            elif value==8:
                mycam.OV2640_set_JPEG_size(OV2640_1600x1200)
            elif value==0x10:
                print('single capture')
                mode=1
                start_capture=1
            elif value==0x11:
                mycam.set_format(JPEG)
                mycam.Camera_Init()
                mycam.set_bit(ARDUCHIP_TIM,VSYNC_LEVEL_MASK)
            elif value==0x20:
                print('stream capture')
                mode=2
                start_capture=2
                stop_flag=0
                httpServer_response_stream_init(cli_sock)
            elif value==0x21:
                stop_flag=1
            elif value==0x30:
                mode=3
                start_capture=3
            elif value==0x40:
                mycam.OV2640_set_Light_Mode(Auto)
            elif value==0x41:
                mycam.OV2640_set_Light_Mode(Sunny)
            elif value==0x42:
                mycam.OV2640_set_Light_Mode(Cloudy)
            elif value==0x43:
                mycam.OV2640_set_Light_Mode(Office)
            elif value==0x44:
                mycam.OV2640_set_Light_Mode(Home)
            elif value==0x50:
                mycam.OV2640_set_Color_Saturation(Saturation2)
            elif value==0x51:
                mycam.OV2640_set_Color_Saturation(Saturation1)
            elif value==0x52:
                mycam.OV2640_set_Color_Saturation(Saturation0)
            elif value==0x53:
                mycam.OV2640_set_Color_Saturation(Saturation_1)
            elif value==0x54:
                mycam.OV2640_set_Color_Saturation(Saturation_2)
            elif value==0x60:
                mycam.OV2640_set_Brightness(Brightness2)
            elif value==0x61:
                mycam.OV2640_set_Brightness(Brightness1)
            elif value==0x62:
                mycam.OV2640_set_Brightness(Brightness0)
            elif value==0x63:
                mycam.OV2640_set_Brightness(Brightness_1)
            elif value==0x64:
                mycam.OV2640_set_Brightness(Brightness_2)
            elif value==0x70:
                mycam.OV2640_set_Contrast(Contrast2)
            elif value==0x71:
                mycam.OV2640_set_Contrast(Contrast1)
            elif value==0x72:
                mycam.OV2640_set_Contrast(Contrast0)
            elif value==0x73:
                mycam.OV2640_set_Contrast(Contrast_1)
            elif value==0x74:
                mycam.OV2640_set_Contrast(Contrast_2)
            elif value==0x80:
                mycam.OV2640_set_Special_effects(Antique);
            elif value==0x81:
                mycam.OV2640_set_Special_effects(Bluish);
            elif value==0x82:
                mycam.OV2640_set_Special_effects(Greenish);
            elif value==0x83:
                mycam.OV2640_set_Special_effects(Reddish);
            elif value==0x84:
                mycam.OV2640_set_Special_effects(BW);
            elif value==0x85:
                mycam.OV2640_set_Special_effects(Negative); 
            elif value==0x86:
                mycam.OV2640_set_Special_effects(BWnegative);
            elif value==0x87:
                mycam.OV2640_set_Special_effects(Normal);
                
        if mode==1:
            if start_capture==1:
                mycam.flush_fifo();
                mycam.clear_fifo_flag();
                mycam.start_capture();
                start_capture=0
            if mycam.get_bit(ARDUCHIP_TRIG,CAP_DONE_MASK)!=0:
                #read_fifo_burst_socket(eth, s)
                httpServer_response_single(cli_sock)
                mode=0
        elif mode==2:
            if stop_flag==0:
                if start_capture==2:
                    start_capture=0
                    mycam.flush_fifo();
                    mycam.clear_fifo_flag();
                    mycam.start_capture();
                if mycam.get_bit(ARDUCHIP_TRIG,CAP_DONE_MASK)!=0:
                    httpServer_response_stream_burst(cli_sock)
                    #read_fifo_burst_socket(eth, s)
                    start_capture=2
            else:
                mode=0
                start_capture=0
        
        if mode == 0:
            if prev_mode != mode:
                print('Stop')
                httpServer_close(cli_sock)
                break

        prev_mode = mode