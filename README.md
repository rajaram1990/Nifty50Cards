#Nifty50Cards
Shows up stock prices of CNX 100 scrips of NSE as cards, letting one sort the cards based on parameters such as top gainers, top losers and top movers. Uses Cherrypy framework and a redis instance as backend

- Rajaram, Jun 2016
- License : GPL v2

## Installation

1. Clone the repository and navigate to the root of the repo
```bash
    git clone https://github.com/rajaram1990/Nifty50Cards.git
    cd Nifty50Cards
```
2. Set it up with the one click install script

### On Ubuntu / Debian based systems:
or anything that uses apt-get as package manager
```bash
    sudo sh setup_ubuntu.sh
```
Feel free to check the contents of setup.sh if you're not very excited about running a random script with sudo

### On CentOS / RHEL based systems:
or anything that uses yum as package manager
```bash
    sudo sh setup_rhel.sh
```
3. Start the cherrypy server to start serving requests
```bash
    python server.py
```
This will run the server with logs on the console. Helps tracing requests and to check the background thread that syncs prices once every 5 mins. Else you could always run it in the background and redirect the output to a file by specifying error file in cherrypy config
```python
    cherrypy.config.update({'log.error_file': Web.log,
                            'log.access_file': Access.log
                            })
```
