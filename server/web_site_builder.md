# Hetnet Web App

## Current Progress Front End
- Using Angular JS to build the single page app
- $Http for JSON Request
- $Scope for basic data storage

## Progress Backend
- Running MongoDB with Node.js

## Requirement (Mac)
[On amazon EC2 machine](http://www.lauradhamilton.com/how-to-set-up-a-nodejs-web-server-on-amazon-ec2)

[Check the Port Working Properly](http://www.yougetsignal.com/tools/open-ports/)

Currently the port working on the Amazon AMI, ubuntu may have port failure.

```python
python -m SimpleHTTPServer 8000
```
Try this to see your port open correctly

### System Environment for Amazon EC 2 (Same as Ubuntu and OSX)
```
sudo apt-get install build-essential curl git python-setuptools ruby

brew install node

brew install mongodb

npm install -g grunt-cli

npm install -g bower

gem install compass

```
### Module in server
```
npm install --save express
npm install --save mongoose
npm install --save resourcejs
npm install --save method-override
npm install --save body-parser
npm install --save lodash
npm install --save helmet
```
## Running order
In order to run this web app, you need mongodb setup in the server and have a DB name "Hetnet"
```
# When you need your app to work in the background 
screen
use ctrl A+D to exit
use exit; to shut down the screen
screen -ls see all sessions
screen -r <number of thread> go to the log
```
### See Port open
```
netstat -ntlp | grep LISTEN
```
