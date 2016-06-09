"""
    Does all steps required for initialising the application
    Fetches list of cnx 50 stocks
    and populates the redis cache
"""
import sys
import requests
import redis
import populate_prices
companies = []
sectors = []
try:
    redis_obj = redis.Redis(host='localhost', port=6379, db=0, password=None)
except Exception, e:
    print >> sys.stderr, """Please ensure redis is running on localhost on 6379.
                         If not change config accordingly"""
    raise(e)

def get_cnx_100_scrips():
    """
        Fetches cnx100 scrips for nseindia.com
        Warning : The link gets depricated pretty often. Watch out for errors
        Order of columns from NSEIndia script:
            0 : Company Name
            1 : Industry
            2 : Symbol
        Stores a redis data structire of the following format:
        'companies' = 'cn1,cn2,cn3'.. #comma separated list of companies
        'sectors' = 's1,s2,s3'.. #Comma separated list of distinct sectors
        'scrips' = 'c1,c2,c3'.. # comma separated list of scrips
        '<c1>:sector'= s1 # Given scrip as key, throws its sector
        '<s1>:companies' : 'c1,c2,c3' # Given sector as key, throws comma sep. list of scrips
        '<c1>:name' : Given c1, throws cn1
        This is better than a json against each company as this approach helps
        retrieval significantly
    """
    companies = []
    sectors = []
    scrips = []
    companies_sector_map = {}
    sector_companies_map = {}
    scrip_company_map = {}
    nseindia_url = 'https://www.nseindia.com/content/indices/ind_niftylist.csv'
    resp = requests.get(nseindia_url)
    if resp.status_code != requests.codes.ok:
        raise Exception('Error fetching scrip from NseIndia')
    content = resp.text
    lines = content.split('\n') # Did not use a csvreader since this is an one off script
    lines = lines[1:]
    for line in lines:
        print line
        line_parts = line.split(',')
        if line_parts and len(line_parts) > 1:
            print line_parts
            companies.append(line_parts[0])
            sectors.append(line_parts[1])
            scrips.append(line_parts[2])
            companies_sector_map[line_parts[2]] = line_parts[1]
            redis_obj.set('%s:sector'%(line_parts[2]),line_parts[1])
            if sector_companies_map.get(line_parts[1]):
                sector_companies_map[line_parts[1]].append(line_parts[2])
            else:
                sector_companies_map[line_parts[1]] = [line_parts[2]]
            scrip_company_map[line_parts[2]] = line_parts[0]
            redis_obj.set('%s:name'%(line_parts[2]),line_parts[0])
    # build redis cache out of local dictionaries
    redis_obj.set('companies',','.join(companies))
    redis_obj.set('scrips',','.join(scrips))
    redis_obj.set('sectors',','.join(list(set(sectors))))
    for k,v in sector_companies_map.iteritems():
        redis_obj.set('%s:companies'%(k),','.join(v))

if __name__ == '__main__':
    get_cnx_100_scrips()
    populate_prices.update_prices()
