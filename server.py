import cherrypy
import os
import redis
import GetNSEStockPrice.get_stock as get_stock
from cherrypy.process.plugins import Monitor
import datetime
import simplejson as json
from collections import OrderedDict

REDIS_OBJ = redis.Redis(host='10.193.124.239', port=6379, db=0)
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
    def GET(self, filter=None):
        """"
            Sort can be on of
            'tm', 'tg', 'tl'
            top movers, top gainers and top losers
        """
        scrip_data = {}
        scrips = REDIS_OBJ.get('scrips').split(',')
        scrip_data['scrips'] = scrips
        for scrip in scrips:
            scrip_data[scrip] = {'company_name' : REDIS_OBJ.get('%s:name'%(scrip)),
                                 'ltp' : REDIS_OBJ.get('%s:ltp'%(scrip)),
                                 'chg' : REDIS_OBJ.get('%s:chg'%(scrip)),
                                 'pc_chg' : REDIS_OBJ.get('%s:pc_chg'%(scrip))
                                }
        if filter:
            change_scrip_map = {} #list of scrips with a particular % change
            for scrip in scrips:
                pc_change = scrip_data[scrip]['pc_chg']
                if filter == 'tg':
                    if pc_change.startswith('-'):
                        continue
                if filter == 'tl':
                    if not pc_change.startswith('-'):
                        continue
                if pc_change.startswith('+') or pc_change.startswith('-'):
                    pc_change = float(pc_change[1:]) # May have conversion issues, but doesn't concern us
                else:
                    pc_change = float(pc_change)
                if change_scrip_map.get(pc_change):
                    change_scrip_map[pc_change].append(scrip)
                else:
                    change_scrip_map[pc_change] = [scrip]
            sorted_pcs = change_scrip_map.keys()
            sorted_pcs.sort(reverse=True)
            print sorted_pcs
            ordered_scrips = []
            for pc in sorted_pcs:
                ordered_scrips.extend(change_scrip_map[pc])
            scrip_data['scrips'] = ordered_scrips
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
    update_prices()
    cherrypy.engine.start()
    cherrypy.engine.block()
