# WeatherCandle - Weather and Temperature at a glance
Using this magic candle, you can tell the current temperature and conditions outside instantly

![Color Range 0 to 100*F](https://raw.githubusercontent.com/khinds10/WeatherJar/master/construction/main-image.png)

![Color Range 0 to 100*F](https://raw.githubusercontent.com/khinds10/WeatherJar/master/construction/range.png)

**Color Range 0 to 100*F**

### Animations in Action

### [![IMAGE ALT TEXT](http://img.youtube.com/vi/RNsYiCd4rvg/0.jpg)](https://www.youtube.com/watch?v=RNsYiCd4rvg "Weather Candle")

#### Flashing RaspberriPi Hard Disk / Install Required Software (Using Ubuntu Linux)

Download "RASPBIAN JESSIE LITE"
https://www.raspberrypi.org/downloads/raspbian/

**Create your new hard disk for DashboardPI**
>Insert the microSD to your computer via USB adapter and create the disk image using the `dd` command
>
> Locate your inserted microSD card via the `df -h` command, unmount it and create the disk image with the disk copy `dd` command
>
> $ `df -h`
> */dev/sdb1       7.4G   32K  7.4G   1% /media/XXX/1234-5678*
>
> $ `umount /dev/sdb1`
>
> **Caution: be sure the command is completely accurate, you can damage other disks with this command**
>
> *if=location of RASPBIAN JESSIE LITE image file*
> *of=location of your microSD card*
>
> $ `sudo dd bs=4M if=/path/to/raspbian-jessie-lite.img of=/dev/sdb`
> *(note: in this case, it's /dev/sdb, /dev/sdb1 was an existing factory partition on the microSD)*

**Setting up your RaspberriPi**

*Insert your new microSD card to the raspberrypi and power it on with a monitor connected to the HDMI port*

Login
> user: **pi**
> pass: **raspberry**

Change your account password for security
>`sudo passwd pi`

Enable RaspberriPi Advanced Options
>`sudo raspi-config`

Choose:
`1 Expand File System`

`9 Advanced Options`
>`A2 Hostname`
>*change it to "WeatherJar"*
>
>`A4 SSH`
>*Enable SSH Server*
>
>`A7 I2C`
>*Enable i2c interface*

**Enable the English/US Keyboard**

>`sudo nano /etc/default/keyboard`

> Change the following line:
>`XKBLAYOUT="us"`

**Reboot PI for Keyboard layout changes / file system resizing to take effect**
>$ `sudo shutdown -r now`

**Auto-Connect to your WiFi**

>`sudo nano /etc/wpa_supplicant/wpa_supplicant.conf`

Add the following lines to have your raspberrypi automatically connect to your home WiFi
*(if your wireless network is named "linksys" for example, in the following example)*

	network={
	   ssid="linksys"
	   psk="WIRELESS PASSWORD HERE"
	}

**Reboot PI to connect to WiFi network**

>$ `sudo shutdown -r now`
>
>Now that your PI is finally on the local network, you can login remotely to it via SSH.
>But first you need to get the IP address it currently has.
>
>$ `ifconfig`
>*Look for "inet addr: 192.168.XXX.XXX" in the following command's output for your PI's IP Address*

**Go to another machine and login to your raspberrypi via ssh**

> $ `ssh pi@192.168.XXX.XXX`

**Start Installing required packages**

>$ `sudo apt-get update`
>
>$ `sudo apt-get upgrade`
>
>$ `sudo apt-get install memcached vim git python-smbus i2c-tools python-imaging python-smbus build-essential python-dev rpi.gpio python3 python3-pip python-memcache`

**Update local timezone settings

>$ `sudo dpkg-reconfigure tzdata`

`select your timezone using the interface`

**Setup the simple directory `l` command [optional]**

>`vi ~/.bashrc`
>
>*add the following line:*
>
>`alias l='ls -lh'`
>
>`source ~/.bashrc`

**Fix VIM default syntax highlighting [optional]**

>`sudo vi  /etc/vim/vimrc`
>
>uncomment the following line:
>
>_syntax on_

**Install i2c Python Drivers**

Install the NeoPixel Driver as follows 

>`sudo apt-get install build-essential python-dev git scons swig`
>
>`sudo pip3 install --upgrade setuptools`
>
>`sudo pip3 install rpi_ws281x`
>
>`cd rpi_ws281x`
>
>`scons`
>
>`cd python`
>
>`sudo python setup.py install`
>
>`cd examples/`
>
>`sudo python strandtest.py`

# Supplies Needed

**RaspberryPi Zero**

![RaspberryPi Zero](https://raw.githubusercontent.com/khinds10/WeatherJar/master/construction/PiZero.jpg)

**USB WIFI (if not a PiZero W)**

![USB WIFI (if not a PiZero W)](https://raw.githubusercontent.com/khinds10/WeatherJar/master/construction/wifi.jpg)

**NeoPixel Ring**

![NeoPixel Ring](https://raw.githubusercontent.com/khinds10/WeatherJar/master/construction/neoring.jpg)

**Frosted Lamp Shade**

![Frosted Lamp Shade](https://raw.githubusercontent.com/khinds10/WeatherJar/master/construction/lamp-shade.png)

# Building the WeatherJar

Solder the leads to connect the NeoPixel Ring to the Pi, needs 5V, GND and GPIO pin 18 connected

*Note: since we're only using one ring with not ever showing full brightness / bright white colors, we can rely on the power source of the RPi itself.  Ordinarily they recommend the 5050 RGB pixesl such as these to have their own power source.

WIRING DIAGRAM HERE

![Internal Assembly](https://raw.githubusercontent.com/khinds10/WeatherJar/master/construction/build/weather-candle0.jpg)

![Internal Assembly](https://raw.githubusercontent.com/khinds10/WeatherJar/master/construction/build/weather-candle1.jpg)

![Wire Power](https://raw.githubusercontent.com/khinds10/WeatherJar/master/construction/build/weather-candle2.jpg)

![Assembly Completed](https://raw.githubusercontent.com/khinds10/WeatherJar/master/construction/build/weather-candle3.jpg)

![Assembly Completed](https://raw.githubusercontent.com/khinds10/WeatherJar/master/construction/build/weather-candle4.jpg)



# Creating the Temperature API

Python Flash API for displaying temperatures as color gradients installation instructions

### Installation

Clone the project webserver folder locally on your webserver from this project [/var/www]

Create the Apache configuration to point to this project (Python Flask API)

Required Packages for Python Flash on Apache

`$> sudo apt-get install libapache2-mod-wsgi python-dev python-pip python-pil`

`$> sudo a2enmod wsgi`

`$> sudo service apache2 restart`

`$> pip install flask`

    <VirtualHost *:80>
        ServerAdmin webmaster@mytempuratureapi.com
        ServerName mytempuratureapi.com
        ServerAlias mytempuratureapi.com
        DocumentRoot /var/www/temperatureapi
        ErrorLog /var/www/temperatureapi/error.log
        CustomLog /var/www/temperatureapi/access.log combined
    
        WSGIDaemonProcess temperatureapp user=khinds group=khinds threads=5
        WSGIProcessGroup temperatureapp
        WSGIScriptAlias / /var/www/temperatureapi/app.wsgi
    
        <Directory /var/www/temperatureapi>
               Require all granted
        </Directory>
    
    </VirtualHost>

You can now ask for RGB NeoPixel color gradients for given environment temperatures

http://mytempuratureapi.com/neopixel?temperature=72

### Set pi user crontab 

Enter the following line for a minute by minute crontab

`$ crontab -e`

`*/1 * * * * python /home/pi/WeatherJar/weather.py`

### Set root user crontab (this library requires root access)

Set "on reboot" to run the candle python script forever

`$ sudo su`

`$ crontab -e`

`@reboot python /home/pi/WeatherJar/candle.py`

**Color Range 0 to 100*F**

![Color Range 0 to 100*F](https://raw.githubusercontent.com/khinds10/WeatherJar/master/webserver/neopixel.png)Be sure to place this new URL you generated in your project settings so you can now have the weather jar respond to your current outdoor temperatures.

# Finished!
