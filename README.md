#Nifty50Cards
Shows up stock prices of CNX 50 scrips of NSE as cards, letting one sort the cards based on parameters such as top gainers, top losers and top movers. Uses Cherrypy framework and a redis instance as backend

- Rajaram, Jun 2016
- License : GPL v2

## Installation

* Clone the repository and navigate to the root of the repo
```bash
    git clone https://github.com/rajaram1990/Nifty50Cards.git
    cd Nifty50Cards
```
* Set it up with the one click install script

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
* Start the cherrypy server to start serving requests
```bash
    python server.py
```
This will run the server with logs on the console on 8080. Helps tracing requests and to check the background thread that syncs prices once every 5 mins. Else you could always run it in the background and redirect the output to a file by specifying error file in cherrypy config
```python
    cherrypy.config.update({'log.error_file': Web.log,
                            'log.access_file': Access.log
                            })
```
You can now access the UI on browser at http://localhost:8080

## Basic Code Flow
As mentioned above, we use a redis instance to persist scrips and current prices. The init script, setup.py (in turn called by setup.sh after installing the necessary software packages including cherrypy and redis), fetches the list of cnx 50 stocks from nseindia.com's csv list. This is then parsed for company name, sector and scrips and is loaded in the redis instance against the key scrips.

server.py consists of the cherrypy backend code that reads the list of scrips from redis against this key and attempts to fetch the current price of the particular scrip using the GetNSEStockPrice library (https://github.com/rajaram1990/GetNSEStockPrice.git) in batches and updates the redis cache against 'scrip_name:ltp', 'scrip_name:chg' and so on. This is done by update_prices method in server.py. This method is called by cherrypy every 5 mins using monitor for auto update of prices as well as whenever the user presses the sync button in UI

The GetScrips class is mounted in cherrypy on /api/cards endpoint. The GET method here simply fetches the list of scrips from redis cache and the prices of each of them from redis and builds a dictionary out of them. The GET method takes a parameter, order, that lets the user specify if she wants top gainers / top losers / top movers. Once we have the dict with the relevant details, we sort the scrips list using the appropriate metric and send the scrips list and the dictionary containing data of all the scrips as a JSON.

User can also perform a post call to GetScrips (or the api/cards endpoint) to get the latest prices after a sync from finance API.

##UI

The UI utilizes Boostrap V4 for layout, typography, nav bar and the cards interface. col-sm-6 splits the entire screen into two parts with appropriate margin, padding etc. To have two cards side by side, it is further split into two col-sm-6 blocks.

The up / down icon and the refresh icon are from fontsawesome since bootstrap v4 does not come with native support for Glyphicons.

All the UI, css, basic jquery events etc. are defined in index.html itself as the jquery is not very elaboraate, but just a few methods to handle events. All cards are housed within a container named refresh_section. Upon clicking any of the buttons in the tab / sync, generate_cards.js is triggered.

The generate_cards.js (public/js/generate_cards.js Excuse me for the naming. It's the consequence of coding python) is the javascript piece that renders these cards as HTML from the json that python returns. It consumes the data from the /api/cards url and scans iteratively over the scrips list (to maintain order) and builds cards from the scrip_data dictionary. There is nothing elaborate here except for some elaborate string building. It keeps appending the output to an output string which is then returned.

The jquery in index.html is configured to alter the HTML of the refresh_section with the html that generate_cards returns, thereby rendering the new set of cards with updated ordering / latest prices.

## Testing the backend API

Simply call http://localhost:8080/api/cards to see the json data that the python API returns.
It contains a lot more data than what is consumed by the cards generator. We'll soon be showing up in the cards as well.

###Other variants:
#### Top Movers
http://localhost:8080/api/cards?order=tm

#### Top Gainers
http://localhost:8080/api/cards?order=tg

#### Top Losers
http://localhost:8080/api/cards?order=tl

