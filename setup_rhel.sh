sudo curl "https://bootstrap.pypa.io/get-pip.py" -o "get-pip.py"
sudo /usr/local/bin/pip install --upgrade pip
sudo /usr/local/bin/pip install GetNSEStockPrices
sudo /usr/local/bin/pip install simplejson
sudo /usr/local/bin/pip install cherrypy
sudo /usr/local/bin/pip install redis
sudo easy_install dateutil
wget http://download.redis.io/releases/redis-3.2.0.tar.gz
tar xzf redis-3.2.0.tar.gz
cd redis-3.2.0
cd deps
sudo make hiredis jemalloc linenoise lua
cd ..
make
sudo cp src/redis-server /usr/local/bin/
sudo cp src/redis-cli /usr/local/bin/
redis-server & 2>&1 > ~/redis_logs
cd ..
python setup.py
