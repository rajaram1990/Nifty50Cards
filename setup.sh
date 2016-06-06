sudo pip install --upgrade pip
sudo pip install GetNSEStockPrices
sudo pip install cherrypy
sudo pip install redis
wget http://download.redis.io/releases/redis-3.2.0.tar.gz
tar xzf redis-3.2.0.tar.gz
cd redis-3.2.0
make
sudo cp src/redis-server /usr/local/bin/
sudo cp src/redis-cli /usr/local/bin/
redis-server & 2>&1 > ~/redis_logs
cd ..
python setup.py
