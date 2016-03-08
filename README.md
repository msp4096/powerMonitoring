### Renda Solar Stuff
Eric's solar thingy.

## Steps to install
Instal the necessary packages  
```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install cmake libusb-1.0-0-dev golang
```
#### RTL-SDR
Download RTL-SDR and build it  
```
git clone git://git.osmocom.org/rtl-sdr.git
cd rtl-sdr/
mkdir build
cd build
cmake ../
make
sudo make install
sudo ldconfig
```
Edit the follwing file as root
```
/etc/modprobe.d/raspi-blacklist.conf
```
and add the line
```
blacklist dvb_usb_rtl28xxu
```
Reboot the system with ```sudo reboot```  
Test the RTL-SDR with ```sudo rtl_test```. If it works, kill it with ```CTRL-C```


#### RTLAMR
Set the GO Path and download RTLARM  
```
export GOPATH=$HOME/go
export PATH=$PATH:$GOROOT/bin:$GOPATH/bin
go get github.com/bemasher/rtlamr
```
Try out rtlamr and rtl-sdr together. Open up two terminals. In the first, do:  
```
sudo rtl_tcp
```
and in the second, do:  
```
/home/pi/go/bin/rtlamr
```  
You should see meter readings popping up in the second terminal. If you do, it's working!  
Kill rtlamr from the first terminal with ```CRTL-C```

#### powerMonitoring
Now, let's clone **your** git repo
```
git clone https://github.com/msp4096/powerMonitoring.git
```
Move some files around and clean up the rest
```
mv go/bin/rtlamr powerMonitoring/
rm -rf go/ rtl-sdr/
```
From here, try to run the script that does everything with:
```
sudo /home/pi/powerMonitoring/meter_read.sh
```
Hunt down any errors that it spits out. If there are no errors, check the log file to see if a new reading was saved. If so, that part works too! Edit cronjob
```
sudo crontab -e
```
and add the following line so the scrip runs on it own. The 15 means it will run every 15 minutes.
```
*/15 * * * * /home/pi/powerMonitoring/meter_read.sh > /home/pi/powerMonitoring/meter_read.log 2>&1
```
Give it 15 minutes, and check to see if another entry was saved to the log file. If so, that's it!

## Useful links
http://sdr.osmocom.org/trac/wiki/rtl-sdr#Buildingthesoftware  
http://bemasher.github.io/rtlamr/
### Other Helpful tips
#### Change the timezone
```sudo dpkg-reconfigure tzdata```
