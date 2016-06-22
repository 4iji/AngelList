#! /usr/bin/env python

import argparse, os, time, pickle
from pprint import pprint
import angellist
from dirUtils import ensure_dir

# Assumes you have an environmental variable called AL_ACCESS_TOKEN exported from your .bashrc, etc.
ACCESS_TOKEN = os.environ['AL_ACCESS_TOKEN']

def main(folder_out):
    ensure_dir(folder_out)
    
    market_names = ['deep learning', 'fintech']
    min_investments = 1
    investor_types = ['User', 'Startup']
    investor_locations = ['london', 'united kingdom']

    market_path = os.path.join(folder_out, 'markets.pickle')
    startup_path = os.path.join(folder_out, 'startups.pickle')
    role_path = os.path.join(folder_out, 'roles.pickle')
    investor_path = os.path.join(folder_out, 'investors.pickle')

    al = angellist.AngelList()
    al.access_token = ACCESS_TOKEN

    # Sanity test
    #my_angel_list_profile = al.getMe()
    #print my_angel_list_profile['bio']

    # Get markets
    if os.path.isfile(market_path):
        markets = pickle.load(open(market_path))
    else:
        markets = list()
        for name in market_names:
            markets += al.getSearch(query = name, type_option = "MarketTag")
        pickle.dump(markets, open(market_path, 'wb'))

    # Get startups in relevant markets
    if os.path.isfile(startup_path):
        startups = pickle.load(open(startup_path))
    else:
        startups = list()
        for market in markets:
            for page in range(1, 9999999):
                result = al.getTags(tag_id = market['id'], domain = 'startups', page = page)
                startups += result['startups']
                if page == 1:
                    print result['last_page']
                if 'last_page' not in result or page == result['last_page']:
                    break
        pickle.dump(startups, open(startup_path, 'wb'))
    # Get investor roles
    if os.path.isfile(role_path):
        roles = pickle.load(open(role_path))
    else:
        failed = list()
        roles = list()
        for startup in startups:
            # Most likely only one page
            try:
                result = al.getStartupRoles(startup_id = startup['id'])
                roles += [role for role in result['startup_roles'] if 'investor' in role['role']]
                time.sleep(2)
            except:
                failed.append(startup['id'])
        pickle.dump(roles, open(role_path, 'wb'))
        # Print failed API calls
        print 'Failed to find the following starups:'
        for id in failed:
            print "/t%d" % id
    # Get investors and aggregate startups they invested in
    investors = dict()
    for role in roles:
        if role['tagged']['id'] not in investors:
            investors[role['tagged']['id']] = (list(), role['tagged'])
        if role['startup']['id'] not in investors[role['tagged']['id']][0]:
            investors[role['tagged']['id']][0].append(role['startup']['id'])
    investor_keys = sorted(investors, key=lambda k: len(investors[k][0]), reverse=True)
    # Print investors
    for kind in investor_types:
        print "\n<<< %s >>>\n" % kind
        i = 0
        for key in investor_keys:
            # Get investor details via API
            try:
                investor = al.getUsers(user_id = key)
            except:
                investor = {'locations': []}
            if investor['locations']:
                locations = [location['name'].lower() for location in investor['locations']]
            else:
                locations = []
            if len(investors[key][0]) < min_investments:
                break
            if (investors[key][1]['type'] == kind and 
                any( [investor_location in location for investor_location in investor_locations for location in locations]) ):
                i += 1
                name = ( investors[key][1]['name'] ).encode('ascii', 'ignore')
                investments = len(investors[key][0])
                quality = investors[key][1]['quality'] if 'quality' in investors[key][1] else None
                if quality:
                    print "%4d \t %s (qual: %s; invest: %s)" % (i, name, quality, investments)
                else:
                    print "%4d \t %s (invest: %s)" % (i, name, investments)
                print "\t\t" + str(locations)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scrape angel_list for investors')
    parser.add_argument('-o','--folder_out', required=True, help='Where to output the results of the AngelList API')
    args = parser.parse_args()

    main(args.folder_out)
