import cherrypy
import os
import redis
import GetNSEStockPrice.get_stock as get_stock
from cherrypy.process.plugins import Monitor
import datetime
import simplejson as json
from collections import OrderedDict

REDIS_OBJ = redis.Redis(host='localhost', port=6379, db=0)
SCRIPS = REDIS_OBJ.get('scrips').split(',')

class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        return open('index.html')

class GetScrips:
    exposed = True
    def GET(self, order=None):
        scrips = REDIS_OBJ.get('scrips').split(',')
        return json.dumps(scrips)

class NSECards:
    exposed = True
    def GET(self, order=None):
        scrip_data = {}
        scrips = REDIS_OBJ.get('scrips').split(',')
        scrip_data['scrips'] = scrips
        for scrip in scrips:
            scrip_data[scrip] = {'company_name' : REDIS_OBJ.get('%s:name'%(scrip)),
                                 'ltp' : REDIS_OBJ.get('%s:ltp'%(scrip)),
                                 'chg' : REDIS_OBJ.get('%s:chg'%(scrip)),
                                 'pc_chg' : REDIS_OBJ.get('%s:pc_chg'%(scrip))
                                }
        return json.dumps(scrip_data)
    def POST(self, order=None):
        update_prices() #calling a post to the same enpoint also syncs the new prices
def update_prices():
    print SCRIPS
    print len(SCRIPS)
    scrips_data = get_stock.get_stock_price(SCRIPS)
    print 'Starting thread at %s'%(datetime.datetime.now())
    for scrip, data in scrips_data.iteritems():
        REDIS_OBJ.set('%s:ltp'%(scrip),data['price'])
        REDIS_OBJ.set('%s:chg'%(scrip), data['change_inr'])
        REDIS_OBJ.set('%s:pc_chg'%(scrip), data['change_pc'])
    print scrips_data


if __name__ == '__main__':
    cherrypy.config.update({'server.socket_host': '0.0.0.0'})
    current_dir = os.path.dirname(os.path.abspath(__file__))
    Monitor(cherrypy.engine, update_prices, frequency=300).subscribe()
    cherrypy.tree.mount(
        NSECards(), '/api/cards',
        {'/':
            {'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
             'tools.sessions.on': True,
             'tools.response_headers.on': True,
             'tools.response_headers.headers': [('Content-Type', 'text/plain')],
            }
        }
    )
    static_conf = {
        '/static': {
             'tools.staticdir.on': True,
             'tools.staticdir.dir': os.path.join(current_dir, 'public')
          }
        }
    cherrypy.tree.mount(
        HelloWorld(), '/', static_conf
    )
    cherrypy.tree.mount(
        GetScrips(), '/api/scrips',
        {'/':
            {'request.dispatch': cherrypy.dispatch.MethodDispatcher(),
             'tools.sessions.on': True,
             'tools.response_headers.on': True,
             'tools.response_headers.headers': [('Content-Type', 'text/plain')],
            }
        })

    cherrypy.engine.start()
    cherrypy.engine.block()
