import cherrypy
import redis
import GetNSEStockPrice.get_stock as get_stock
from cherrypy.process.plugins import Monitor
import datetime
import simplejson as json

songs = {
    '1': {
        'title': 'Lumberjack Song',
        'artist': 'Canadian Guard Choir'
    },

    '2': {
        'title': 'Always Look On the Bright Side of Life',
        'artist': 'Eric Idle'
    },

    '3': {
        'title': 'Spam Spam Spam',
        'artist': 'Monty Python'
    }
}
REDIS_OBJ = redis.Redis(host='localhost', port=6379, db=0)
SCRIPS = REDIS_OBJ.get('scrips').split(',')

class HelloWorld(object):
    @cherrypy.expose
    def index(self):
        return "Hello world!"

class NSECards:

    exposed = True

    def GET(self, id=None):
        scrip_data = {}
        scrips = REDIS_OBJ.get('scrips').split(',')
        for scrip in scrips:
            scrip_data[scrip] = {'company_name' : REDIS_OBJ.get('%s:name'%(scrip)),
                                 'ltp' : REDIS_OBJ.get('%s:ltp'%(scrip)),
                                 'chg' : REDIS_OBJ.get('%s:chg'%(scrip)),
                                 'pc_chg' : REDIS_OBJ.get('%s:pc_chg'%(scrip))
                                }
        return json.dumps(scrip_data)
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
    cherrypy.tree.mount(
        HelloWorld(), '/',{}
    )
    cherrypy.engine.start()
    cherrypy.engine.block()
