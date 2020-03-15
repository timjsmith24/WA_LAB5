# wa_lab.py


## Requirements

This script was written to use python version 2.7 that comes installed default with mac os. To preform a ssh connection to network devices the paramiko module will need to be installed.  
This module is needed in order to run this script. Please see the Setup Section at the bottom for instructions on installing the needed module. 

With paramiko installed, open wa_lab.py with a text editor and edit lines 11-13 with the APs IP address, username, and user password. 
lines 14-15 allow you to set the random min and max times that will be used in the script. Once these lines are edited to your liking you can save the updated script.

```python
host = "192.168.1.146"
user = 'admin'
pw = 'admin1234'
min_time = 10
max_time = 60
```

## How to run the script
You can start the script, using terminal, by entering ```python wa_lab.py``` in the directory of the python script. The script will start.
```
Establishing Connection with 192.168.1.146
Enter q to exit Lab: 
```
While in this state the script will repeat a loop of picking a random number between the set min and max numbers, wait the random number of seconds and then alternate the power level of Radio 2 between 1 and 30. 

To end the script you must type 'q' or you will recieve an ```invalid entry``` error. Once q is typed and entered the following message will come up. Once the next power change is made the ssh connection will end and display the 'Connection Closed' message and the script will end.
```
The script will quit when time runs out on this round
** Connection Closed **
```

<p align="center">
<img src="../master/images/wifi_explorer.png" alt="wifi explorer image" height="400px">
</p>


## How it works 
The main sections of the script are listed here.
```python
def check_break():
def run_wa_lab5(netconnect):
def establish_connection():
def radio_change(chan, radiostatus):
def close(netconnect):
def main():
```
```python 
def main():
```
As named, this is the main section of the script. The script actually starts here and will call the other functions. The functions will establish the ssh connection to the AP, starts a seperate thread to the ```check_break()``` function, then passes the ssh session to the ```run_wa_lab5()``` function. Once the global variable ```quit_lab``` is changed to True in the ```check_break()``` function the ```run_wa_lab5()``` function will complete. Then the main function will then proceed and pass the ssh session to the ```close()``` function. This will close the ssh session to the AP.

```python
def establish_connection():
```
This function sets up the ssh session, puts it in enable mode and takes the session to the int radio 2 configuration of the AP.

```python 
def check_break():
```
This function displays the ```Enter q to exit Lab:``` in the terminal. If anything other than 'q' is entered the function displays ```invalid entry``` and then repeats. Once 'q' is entered the function flips the global variable ```quit_lab``` to True.

```python
def run_wa_lab5(netconnect):
```
This function, when first ran sets a variable ```radiostatus``` to 1. This represents setting the power level to 30. It then proceeds in a loop.  
This loop will check the global variable ```quit_lab``` to see if it is True. If not it will pick a random number between the set min and max values entered, sleep for that amount of seconds and then call the ```radio_change``` function, passing the ssh session and the ```radiostatus``` variable to it. Once that function completes it repeats the loop.  
Once the global variable ```quit_lab``` is True the function will pass back the ssh session and complete

```python
def radio_change(chan, radiostatus):
```
This function checks the status of ```radiostatus```, if it is set to 1 it will send the command to set the power to 30 and commit. it will then flip ```radiostatus``` to 0 and return the ssh session and ```radiostatus``` to the ```run_wa_lab5()``` loop. if ```radiostatus``` is set to 0, it send the command to set the power to 1, commit, flip the ```radiostatus``` to 1, then send the ssh session and ```radiostatus``` back to the ```run_wa_lab5()``` loop.

```python
def close(netconnect):
```
This function closes the ssh session and displays ```** Connection Closed **``` in the terminal.


## Setup

pip can be used to install modules but that will need to be installed on the mac if it currently is not. 

To check if pip is currently installed, in Terminal run ```pip --version```. If pip is installed a version number will be in the response. If pip is not installed it can be installed by running ```curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py``` followed by ```python get-pip.py```

> credit [blog](https://ahmadawais.com/install-pip-macos-os-x-python/) - can view for more detailed instructions

Once pip is installed, you can install the paramiko module. 

```pip install paramiko```
