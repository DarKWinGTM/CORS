import os
import re
import sys
import glob
import time
import json
import pytz
import uuid
import base64
import random
import logging
import _thread
import datetime
import resource
import requests
#   import grequests
import collections
import cloudscraper
#   from replit import db 
from inspect import currentframe as SourceCodeLine
from flask import Flask, json, jsonify, request, redirect, session, send_from_directory, Response, make_response, render_template
import gc

timedate = datetime.datetime
timezone = pytz.timezone

app = Flask(
    __name__, 
    static_url_path = '', 
    static_folder   = 'static',
    template_folder = 'templates'
)

log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

class style():
    BLACK       = '\033[30m'
    RED         = '\033[31m'
    ORANGE      = '\033[91m'
    GREEN       = '\033[32m'
    YELLOW      = '\033[33m'
    BLUE        = '\033[34m'
    MAGENTA     = '\033[35m'
    CYAN        = '\033[36m'
    WHITE       = '\033[37m'
    UNDERLINE   = '\033[4m'
    RESET       = '\033[0m'




CONFIGDB = {
    'THREAD'    : 4, 
    'WORKED'    : 0, 
    'PORT'      : 3000,
    'DB'        : 'proxy.json',
    'WB'        : 'waxid.json'
}

if not os.path.isfile( f'proxy.json' ): open(f'{ CONFIGDB["DB"] }', 'w').write(json.dumps({}, indent = 4))
if not os.path.isfile( f'waxid.json' ): open(f'{ CONFIGDB["WB"] }', 'w').write(json.dumps({}, indent = 4))

''' ### PROXY DB TEMPLATE
DATABASE = {
    '127.0.0.1' : {
        'protocol'  : 'http', 
        'port'      : 80
    }
}
WAXIDDAT = {
    'xxxxx.wam' : {
        'cosig'     : 20
    }
}
.json()['stats']['cosign_remaining_txs']
'''
try:
    DATABASE = json.load(open( f'{ CONFIGDB["DB"] }' ))
    WAXIDDAT = json.load(open( f'{ CONFIGDB["WB"] }' ))
except:
    open(f'{ CONFIGDB["DB"] }', 'w').write(json.dumps(
        json.load(open( f'{ CONFIGDB["DB"] }'.replace('.json', '.source.json') )), 
        indent = 4
    ))
    open(f'{ CONFIGDB["WB"] }', 'w').write(json.dumps({}, indent = 4))
finally:
    DATABASE = json.load(open( f'{ CONFIGDB["DB"] }' ))
    WAXIDDAT = json.load(open( f'{ CONFIGDB["WB"] }' ))

class THREAD():
    def __init__(
        self, 
        digi = 6
    ):
    
        global DATABASE
        global CONFIGDB

        self.digi = digi
        
    def cooldown(
        self
    ):
        global DATABASE
        global CONFIGDB
        
        time.sleep(self.digi)
        
        if CONFIGDB['WORKED'] <= 0:
            CONFIGDB['WORKED'] = 0
        else:
            CONFIGDB['WORKED'] -= 1

class POOL():
    def __init__(
        self, 
        url         = '', 
        uid         = '', 
        method      = 'GET', 
        headers     = {}, 
        cookies     = {}, 
        form        = None, 
        json        = {}, 
        args        = None
    ):
    
        global DATABASE
        global CONFIGDB
        
        self.url        = url
        self.uid        = uid
        self.form       = form
        self.json       = json
        self.args       = args
        self.method     = method
        self.headers    = headers
        self.cookies    = cookies

        self.PROCESS = {
            'get' : [{
                'request' : None, 
                'content' : {}, 
                'rescode' : 999
            }], 
            'post' : [{
                'request' : None, 
                'content' : {}, 
                'rescode' : 999
            }], 
            'find' : [{
                'request' : None, 
                'content' : {}, 
                'rescode' : 999
            }, {
                'request' : None, 
                'content' : {}, 
                'rescode' : 999
            }], 
            'ping' : [{
                'request' : None, 
                'content' : {}, 
                'rescode' : 999
            }], 
            'list' : [{
                'request' : None, 
                'content' : {}, 
                'rescode' : 999
            }]
        }
    
        
    def thread(
        self
    ):
        if self.method == 'POST':
            _thread.start_new_thread(self.post, ())
        else:
            _thread.start_new_thread(self.get, ())
        return
        
    def get(
        self
    ):

        global DATABASE
        global CONFIGDB

        try:
            open(f'ticket/{ self.uid }', 'w').write(json.dumps({
                'url'       : self.url, 
                'form'      : self.form, 
                'json'      : self.json, 
                'args'      : self.args, 
                'headers'   : self.headers, 
                'method'    : self.method, 
                'cookies'   : self.cookies
            }, indent = 4))
        except:
            pass
        finally:
            if CONFIGDB['WORKED'] <= 0:
                CONFIGDB['WORKED'] = 0
            else:
                CONFIGDB['WORKED'] -= 1
            
        return

    def rngs(
        self
    ):

        global DATABASE
        global CONFIGDB
        global WAXIDDAT
      
        try:
            self.proxy = random.choice([
                IP for IP in DATABASE if DATABASE[ IP ]['work'] == True and not re.search('packetstream|geonode', IP)
            ] * 86 + [
                IP for IP in DATABASE if DATABASE[ IP ]['work'] == True and re.search('packetstream', IP)
            ] * 8 + [
                IP for IP in DATABASE if DATABASE[ IP ]['work'] == True and re.search('geonode', IP)
            ] * 52 + [
                IP for IP in DATABASE if DATABASE[ IP ]['work'] == 429 and not re.search('packetstream|geonode', IP)
            ] * 1 + [
                None
            ] * 0)
            
            if re.search('packetstream', self.proxy ):
              self.pross = re.sub('@', f'_session-A{ str(timedate.now().timestamp()).replace(".", "")[-7:] }@', self.proxy )
              self.prort = DATABASE[ self.proxy ]["port"]
            elif re.search('geonode', self.proxy ):
              self.pross = re.sub('https\d{4,4}|socks\d{3,4}', '', self.proxy )
              self.prort = f'{DATABASE[ self.proxy ]["port"]}{random.randrange(0, 32):02d}'
            else:
              self.pross = self.proxy
              self.prort = DATABASE[ self.proxy ]["port"]
        except:
            print(f'ERROR self.rngs() { SourceCodeLine().f_lineno }')
            self.proxy = None
            self.pross = None
            
        return f'{ DATABASE[ self.proxy ]["type"] }://{ self.pross }:{ self.prort }'

    #   def rnga(
    #       self
    #   ):
    #   
    #       global DATABASE
    #       global CONFIGDB
    #       global WAXIDDAT
    #     
    #       try:
    #           self.proxy = random.choice([
    #               IP for IP in DATABASE if DATABASE[ IP ]['work'] == True and not re.search('packetstream|geonode', IP)
    #           ] * 128 + [
    #               IP for IP in DATABASE if DATABASE[ IP ]['work'] == True and re.search('packetstream', IP)
    #           ] * 0 + [
    #               IP for IP in DATABASE if DATABASE[ IP ]['work'] == True and re.search('geonode', IP)
    #           ] * 0 + [
    #               IP for IP in DATABASE if DATABASE[ IP ]['work'] == 429 and not re.search('packetstream|geonode', IP)
    #           ] * 0 + [
    #               None
    #           ] * 0)
    #           
    #           if re.search('packetstream', self.proxy ):
    #             self.pross = re.sub('@', f'_session-A{ str(timedate.now().timestamp()).replace(".", "")[-7:] }@', self.proxy )
    #             self.prort = DATABASE[ self.proxy ]["port"]
    #           elif re.search('geonode', self.proxy ):
    #             self.pross = re.sub('https\d{4,4}|socks\d{3,4}', '', self.proxy )
    #             self.prort = f'{DATABASE[ self.proxy ]["port"]}{random.randrange(0, 50):02d}'
    #           else:
    #             self.pross = self.proxy
    #             self.prort = DATABASE[ self.proxy ]["port"]
    #       except:
    #           print(f'ERROR self.rngs() { SourceCodeLine().f_lineno }')
    #           self.proxy = None
    #           self.pross = None
    #           
    #       return f'{ DATABASE[ self.proxy ]["type"] }://{ self.pross }:{ self.prort }'
    
    def post(
        self
    ):

        global DATABASE
        global CONFIGDB
        global WAXIDDAT
        
        try:
            self.rngs()
        except:
            print(f'                                                                                          ERROR self.rngs() { SourceCodeLine().f_lineno }')
            self.proxy = None
        
        try:
            #   if not re.search(
            #       self.json['account_name'], 
            #       open(f'{ CONFIGDB["WB"] }'.replace('.json', '.noop')).read()
            #   ) or ((
            #       WAXIDDAT.get( self.json['account_name'] )
            #   ) or (
            #       WAXIDDAT.get( self.json['account_name'] ) and WAXIDDAT[ self.json['account_name'] ][ 'cosig' ] >= 1
            #   )):
            if not re.search(
                self.json['account_name'], 
                open(f'{ CONFIGDB["WB"] }'.replace('.json', '.noop')).read()
            ):
                try:

                    self.PROCESS['post'][0]['allowag'] = open('webagent.yes').readlines()
                    self.PROCESS['post'][0]['blockag'] = open('webagent.not').readlines()
                    try:
                        #   self.PROCESS['post'][0]['usageag'] = [
                        #       self.post_usageag for self.post_usageag in self.PROCESS['post'][0]['allowag'] if not self.post_usageag in self.PROCESS['post'][0]['blockag']
                        #   ]
                        self.PROCESS['post'][0]['usageag'] = {
                            'custom' : random.choice( self.post_usageag for self.post_usageag in self.PROCESS['post'][0]['allowag'] if not self.post_usageag in self.PROCESS['post'][0]['blockag'] ).strip()
                        }
                    except:
                        self.PROCESS['post'][0]['usageag'] = {
                            'browser' : 'chrome'
                        }
                    #   print( self.PROCESS['post'][0]['usageag'] )

                    self.PROCESS['post'][0]['request'] = cloudscraper.create_scraper(
                        browser = self.PROCESS['post'][0]['usageag'], 
                        delay   = 10
                    ).post(
                        f'{ self.url }',
                        headers = {
                            'authority'             : self.headers['Authority'],        #   'aw-guard.yeomen.ai',
                            'pragma'                : self.headers['Pragma'],           #   'no-cache',
                            'cache-control'         : self.headers['Cache-Control'],    #   'no-cache',
                            'accept'                : self.headers['Accept'],           #   '*/*',
                            'sec-gpc'               : self.headers['Sec-Gpc'],          #   '1',
                            'origin'                : self.headers['Origin'],           #   'https://play.alienworlds.io',
                            'referer'               : self.headers['Referer']           #   'https://play.alienworlds.io/'
                        },
                        json    = self.json,
                        proxies = None if self.proxy == None else {
                            'http'      : f'{ DATABASE[ self.proxy ]["type"] }://{ self.pross }:{ self.prort }',
                            'https'     : f'{ DATABASE[ self.proxy ]["type"] }://{ self.pross }:{ self.prort }'
                        }, 
                        timeout = 15
                    )
                    if self.PROCESS['post'][0]['request'].status_code == 403:
                        try:
                            open('webagent.not', 'a').write( self.PROCESS['post'][0]['request'].request.headers['User-Agent'] + '\n' )
                        except:
                            pass
                    if not re.search('packetstream|geonode', str(self.proxy)) and not self.proxy == None and self.PROCESS['post'][0]['request'].status_code == 200:
                        DATABASE.update({
                            self.proxy : {
                                'type' : DATABASE[ self.proxy ]["type"], 
                                'port' : self.prort, 
                                'work' : True
                            }
                        })
                    elif not re.search('packetstream|geonode', str(self.proxy)) and not self.proxy == None and self.PROCESS['post'][0]['request'].status_code == 429 and random.randrange(100) >= 60:
                        DATABASE.update({
                            self.proxy : {
                                'type' : DATABASE[ self.proxy ]["type"], 
                                'port' : self.prort, 
                                'work' : 429
                            }
                        })
                    elif not re.search('packetstream|geonode', str(self.proxy)) and not self.proxy == None and random.randrange(100) >= 60:
                        DATABASE.update({
                            self.proxy : {
                                'type' : DATABASE[ self.proxy ]["type"], 
                                'port' : self.prort, 
                                'work' : False
                            }
                        })
                except Exception as e:
                    print( f'                                                                                                                        ERROR self.post() { SourceCodeLine().f_lineno } { CONFIGDB["WORKED"] } { self.uid }', str(e)[0:24], self.PROCESS['post'][0]['request'] )
                    if not re.search('packetstream|geonode', str(self.proxy)) and not self.proxy == None and random.randrange(100) >= 60:
                        DATABASE.update({
                            self.proxy : {
                                'type' : DATABASE[ self.proxy ]["type"], 
                                'port' : self.prort, 
                                'work' : None
                            }
                        })
                        
                try     : print( f'                                                                                                                        ONGET self.post() { SourceCodeLine().f_lineno } { CONFIGDB["WORKED"] } { self.uid }', self.url, f'{ DATABASE[ self.proxy ]["type"] }://{ self.pross[0:15] }:{ self.prort }')
                except  : print( f'                                                                                                                        ONGET self.post() { SourceCodeLine().f_lineno } { CONFIGDB["WORKED"] } { self.uid }', self.url, f'replit://localhost:port', self.PROCESS['post'][0]['request'])
                
                try     : print( f'                                                                                                                        ONGET self.post() { SourceCodeLine().f_lineno } { CONFIGDB["WORKED"] } { self.uid }', self.PROCESS['post'][0]['request'] )
                except  : print( f'                                                                                                                        ERROR self.post() { SourceCodeLine().f_lineno } { CONFIGDB["WORKED"] } { self.uid }', self.PROCESS['post'][0]['request'] )
                
            #   elif ((
            #       WAXIDDAT.get( self.json['account_name'] )
            #   ) or (
            #       WAXIDDAT.get( self.json['account_name'] ) and WAXIDDAT[ self.json['account_name'] ][ 'cosig' ] == 0
            #   )) and re.search(
            #       self.json["account_name"], 
            #       open(f'{ CONFIGDB["WB"] }'.replace('.json', '.noop'), 'r').read()
            #   ):
            #       try     : WAXIDDAT.pop( self.json['account_name'] )
            #       except  : pass
            #       
            #       open(f'{ CONFIGDB["WB"] }', 'w').write(json.dumps(WAXIDDAT, indent = 4))
                
            if re.search('aw-guard.yeomen.ai', self.url):
                try     :
                    if (
                        WAXIDDAT.get(self.json['account_name']) and WAXIDDAT[self.json['account_name']]['cosig'] == 0
                    ):
                    #    or (WAXIDDAT.get(self.json['account_name']) == None and re.search(
                    #       self.json["account_name"], 
                    #       open(f'{ CONFIGDB["WB"] }'.replace('.json', '.noop'), 'r').read()
                    #   )):
                        self.PROCESS['post'][0]['content'] = {
                            "uniqid"                : "",
                            "account"               : "",
                            "enabled"               : False,
                            "contract_account"      : "",
                            "contract_action"       : "",
                            "contract_permission"   : "",
                            "buyram_bytes"          : "",
                            "account_tag_exists"    : False,
                            "stats"                 : {
                                "error"                 : None,
                                "errorCode"             : None,
                                "message"               : "",
                                "cosign"                : False,
                                "buyram"                : False,
                                "cosign_remaining_txs"  : 0,
                                "cosign_ratelimit_txs"  : 0
                            }, 
                            'ipport'                 : f'{ DATABASE[ self.proxy ]["type"] }://{ self.pross }:{ self.prort }'
                        }

                        try     : 
                            if not re.search(
                                self.json["account_name"], 
                                open(f'{ CONFIGDB["WB"] }'.replace('.json', '.noop'), 'r').read()
                            ):
                                open(f'{ CONFIGDB["WB"] }'.replace('.json', '.noop'), 'a').write(f'{ self.json["account_name"] },')
                        except  : pass
                        
                        try     : WAXIDDAT.pop( self.json['account_name'] )
                        except  : pass

                        open(f'{ CONFIGDB["WB"] }', 'w').write(json.dumps(WAXIDDAT, indent = 4))

                    else:
                            
                        self.PROCESS['post'][0]['content'] = self.PROCESS['post'][0]['request'].json()
                        self.PROCESS['post'][0]['content']['ipport'] = f'{ DATABASE[ self.proxy ]["type"] }://{ self.pross }:{ self.prort }'
        
                        WAXIDDAT.update({
                            self.json['account_name'] : {
                                'cosig' : self.PROCESS['post'][0]['content'][ 'stats' ]['cosign_remaining_txs']
                            }
                        })
          
                        if not re.search(
                            self.json["account_name"], 
                            open(f'{ CONFIGDB["WB"] }'.replace('.json', '.noop'), 'r').read()
                        ) and WAXIDDAT[ self.json['account_name'] ]['cosig'] == 0:
                            
                            open(f'{ CONFIGDB["WB"] }'.replace('.json', '.noop'), 'a').write(f'{ self.json["account_name"] },')
                            try     : WAXIDDAT.pop( self.json['account_name'] )
                            except  : pass
                        
                        open(f'{ CONFIGDB["WB"] }', 'w').write(json.dumps(WAXIDDAT, indent = 4))

                except Exception as e:

                    #  print( f'ERROR self.post() { SourceCodeLine().f_lineno } { self.uid }', e)
                    
                    if re.search(
                        self.json["account_name"], 
                        open(f'{ CONFIGDB["WB"] }'.replace('.json', '.noop'), 'r').read()
                    ):
                    
                        self.PROCESS['post'][0]['content'] = {
                            "uniqid"                : "",
                            "account"               : "",
                            "enabled"               : False,
                            "contract_account"      : "",
                            "contract_action"       : "",
                            "contract_permission"   : "",
                            "buyram_bytes"          : "",
                            "account_tag_exists"    : False,
                            "stats"                 : {
                                "error"                 : None,
                                "errorCode"             : None,
                                "message"               : "",
                                "cosign"                : False,
                                "buyram"                : False,
                                "cosign_remaining_txs"  : 0,
                                "cosign_ratelimit_txs"  : 0
                            }, 
                            'ipport'                 : f'{ DATABASE[ self.proxy ]["type"] }://{ self.pross }:{ self.prort }'
                        }
                    else:
                        # REGENERATE PROXY
                        self.rngs()
                        self.PROCESS['post'][0]['content'] = {
                            "uniqid"                : "",
                            "account"               : "",
                            "enabled"               : False,
                            "contract_account"      : "",
                            "contract_action"       : "",
                            "contract_permission"   : "",
                            "buyram_bytes"          : "",
                            "account_tag_exists"    : False,
                            "stats"                 : {
                                "error"                 : None,
                                "errorCode"             : None,
                                "message"               : "",
                                "cosign"                : False,
                                "buyram"                : False,
                                "cosign_remaining_txs"  : -1,
                                "cosign_ratelimit_txs"  : -1
                            }, 
                            'ipport'                 : f'{ DATABASE[ self.proxy ]["type"] }://{ self.pross }:{ self.prort }'
                        }
                
                open(f'ticket/{ self.uid }', 'w').write(json.dumps(self.PROCESS['post'][0]['content'], indent = 4))
                return

            else:

                self.PROCESS['post'][0]['content'] = self.PROCESS['post'][0]['request'].text if not (
                    self.PROCESS['post'][0]['request'].headers.get('content-type') == 'application/json'
                ) else self.PROCESS['post'][0]['request'].json()
                
                open(f'ticket/{ self.uid }', 'w').write(json.dumps(self.PROCESS['post'][0]['content'], indent = 4))
                return
              
        except Exception as e:
            
            #  print( f'ERROR self.post() { SourceCodeLine().f_lineno } { self.uid }', self.PROCESS['post'])
            #  
            #  try     : print( f'ERROR self.post() { SourceCodeLine().f_lineno } { self.uid }', self.PROCESS['post'][0]['request'].text)
            #  except  : print( f'ERROR self.post() { SourceCodeLine().f_lineno } { self.uid }', "self.PROCESS['post'][0]['request'].text")
            #  try     : print( f'ERROR self.post() { SourceCodeLine().f_lineno } { self.uid }', self.PROCESS['post'][0]['request'].json())
            #  except  : print( f'ERROR self.post() { SourceCodeLine().f_lineno } { self.uid }', "self.PROCESS['post'][0]['request'].json()")
            #  try     : print( f'ERROR self.post() { SourceCodeLine().f_lineno } { self.uid }', self.PROCESS['post'][0]['request'].headers.get('content-type'))
            #  except  : print( f'ERROR self.post() { SourceCodeLine().f_lineno } { self.uid }', "self.PROCESS['post'][0]['request'].headers.get('content-type')")

            print( f'                                                                                                                        ERROR self.post() { SourceCodeLine().f_lineno } { self.uid }', self.url, e)

            open(f'ticket/{ self.uid }', 'w').write(json.dumps({
                'url'       : self.url, 
                'form'      : self.form, 
                'json'      : self.json, 
                'args'      : self.args, 
                'headers'   : self.headers, 
                'method'    : self.method, 
                'cookies'   : self.cookies, 
                'code'      : 204, 
                'text'      : f'HOSTING CAN NOT COMPLETE {e}'
            }, indent = 4))
            return
        finally:
                
            if CONFIGDB['WORKED'] <= 0:
                CONFIGDB['WORKED'] = 0
            else:
                CONFIGDB['WORKED'] -= 1

    def find(
        self
    ):
        global DATABASE
        global CONFIGDB
        
        while True:
            
            #   try:
            #       self.PROCESS["find"][1]["content"] = json.load(open( f'{ CONFIGDB["DB"] }' ))
            #   except Exception as e:
            #       time.sleep(2)
            #       continue
            #       print( f'ERROR self.list() { SourceCodeLine().f_lineno }', e )
            
            try:
                DATABASE = json.load(open( f'{ CONFIGDB["DB"] }' ))
            except Exception as e:
                if random.randrange(0, 100) >= 16:
                    time.sleep(2); continue
                else:
                    #  os.popen('refresh'); time.sleep(10); continue
                    open(f'{ CONFIGDB["DB"] }', 'w').write(json.dumps(
                        json.load(open( f'{ CONFIGDB["DB"] }'.replace('.json', '.source.json') )), 
                        indent = 4
                    ))
                    time.sleep(2); continue
            
            try:
                if len([ x for x in DATABASE if DATABASE[x]['work'] == True ]) < 128:
                    for count in range(0, 6):
                        #   for self.PROCESS['find'][0]['proxy'] in cloudscraper.create_scraper(
                        #       delay   = 8
                        #   ).get(
                        #       random.choice([
                        #           'https://cors.bridged.cc/https://gimmeproxy.com/api/getProxy?curl=true&supportsHttps=true&referer=true&post=true'
                        #       ] * 3 + [
                        #           'https://cors.bridged.cc/http://pubproxy.com/api/proxy?format=json&https=true&post=true&user_agent=true&referer=true'
                        #       ] * 0), 
                        #       headers = {
                        #           'x-requested-with'      : 'XMLHttpRequest',
                        #           'x-cors-grida-api-key'  : '61dbebf9-36c6-45c6-909e-323209a8116d',
                        #       },
                        #       timeout = 8
                        #   ):  
                        #       
                        #       print( f'FOUND self.find() { SourceCodeLine().f_lineno }', self.PROCESS['find'][0]['proxy'] )
                        #       print( f'FOUND self.find() { SourceCodeLine().f_lineno }', self.PROCESS['find'][0]['proxy'] )
                        #       print( f'FOUND self.find() { SourceCodeLine().f_lineno }', self.PROCESS['find'][0]['proxy'] )
                        #       print( f'FOUND self.find() { SourceCodeLine().f_lineno }', self.PROCESS['find'][0]['proxy'] )
                        #       print( f'FOUND self.find() { SourceCodeLine().f_lineno }', self.PROCESS['find'][0]['proxy'] )
                        #       
                        #       #   https://github.com/ShiftyTR/Proxy-List
                        #       #   {"data":[{"ipPort":"186.226.185.82:666","ip":"186.226.185.82","port":"666","country":"BR","last_checked":"2021-12-18 09:36:30","proxy_level":"anonymous","type":"http","speed":"9","support":{"https":1,"get":1,"post":1,"cookies":1,"referer":1,"user_agent":1,"google":0}}],"count":1}
                        #       if not (
                        #           DATABASE.get( self.PROCESS['find'][0]['proxy'].decode().split('<')[0].split(':')[1].replace('//', '') )
                        #       ) or ((
                        #               DATABASE.get( self.PROCESS['find'][0]['proxy'].decode().split('<')[0].split(':')[1].replace('//', '') )
                        #       ) and (
                        #           DATABASE[ self.PROCESS['find'][0]['proxy'].decode().split('<')[0].split(':')[1].replace('//', '') ]['work'] == False
                        #       )):
                        #           DATABASE.update({
                        #               self.PROCESS['find'][0]['proxy'].decode().split('<')[0].split(':')[1].replace('//', '') : {
                        #                   'type' : self.PROCESS['find'][0]['proxy'].decode().split('<')[0].split(':')[0], 
                        #                   'port' : self.PROCESS['find'][0]['proxy'].decode().split('<')[0].split(':')[2], 
                        #                   'work' : None
                        #               }
                        #           })
                        #           print( f'FOUND self.find() { SourceCodeLine().f_lineno }', self.PROCESS['find'][0]['proxy'].decode().split('<')[0].split(':')[1].replace('//', '') )
                        
                        #   self.rnga()
                        #   
                        #   print( f'{ DATABASE[ self.proxy ]["type"] }://{ self.pross }:{ self.prort }' )
                        #   print( f'{ DATABASE[ self.proxy ]["type"] }://{ self.pross }:{ self.prort }' )
                        #   print( f'{ DATABASE[ self.proxy ]["type"] }://{ self.pross }:{ self.prort }' )
                        #   print( f'{ DATABASE[ self.proxy ]["type"] }://{ self.pross }:{ self.prort }' )
                        #   print( f'{ DATABASE[ self.proxy ]["type"] }://{ self.pross }:{ self.prort }' )
                        
                        try:
                            self.PROCESS['find'][0]['proxy'] = cloudscraper.create_scraper().get(
                                random.choice([
                                    'https://cors.bridged.cc/https://gimmeproxy.com/api/getProxy?curl=true&supportsHttps=true&referer=true&post=true'
                                ] * 1 + [
                                    'http://pubproxy.com/api/proxy?api=VlRnRDY0SjJZRldkOEZqVEw1a2ZKZz09&format=json&https=true&post=true&user_agent=true&referer=true'
                                ] * 0 + [
                                    'https://api.proxyflow.io/v1/proxy/random?token=a294cff1a39b293ada4e2e2a&ssl=true&referer=true&post=true'
                                ] * 5), 
                                cookies = {
                                    'cookieconsent_status'          : 'dismiss'
                                },
                                headers = {
                                    "accept"                        : "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
                                    "accept-language"               : "en-US,en;q=0.9",
                                    "cache-control"                 : "no-cache",
                                    "pragma"                        : "no-cache",
                                    "sec-ch-ua"                     : "\"Chromium\";v=\"96\", \"Opera\";v=\"82\", \";Not A Brand\";v=\"99\"",
                                    "sec-ch-ua-mobile"              : "?0",
                                    "sec-ch-ua-platform"            : "Linux",
                                    "sec-fetch-dest"                : "document",
                                    "sec-fetch-mode"                : "navigate",
                                    "sec-fetch-site"                : "none",
                                    "sec-fetch-user"                : "?1",
                                    "upgrade-insecure-requests"     : "1",
                                    "cookie"                        : "cookieconsent_status=dismiss",
                                    'x-requested-with'              : 'XMLHttpRequest',
                                    'x-cors-grida-api-key'          : '61dbebf9-36c6-45c6-909e-323209a8116d'
                                },
                                timeout = 15
                            )
                        except Exception as e:
                            print( f'ERROR self.find() { SourceCodeLine().f_lineno }', e )
                            time.sleep(1)
                            continue
                        #   https://github.com/ShiftyTR/Proxy-List
                        #   {"data":[{"ipPort":"186.226.185.82:666","ip":"186.226.185.82","port":"666","country":"BR","last_checked":"2021-12-18 09:36:30","proxy_level":"anonymous","type":"http","speed":"9","support":{"https":1,"get":1,"post":1,"cookies":1,"referer":1,"user_agent":1,"google":0}}],"count":1}

                        try:
                            if re.search(
                                'gimmeproxy.com', 
                                self.PROCESS['find'][0]['proxy'].request.url
                            ) and ((
                                DATABASE.get( self.PROCESS['find'][0]['proxy'].content.decode('UTF-8').split('<')[0].split(':')[1].replace('//', '') ) == None
                            ) or (
                                not DATABASE.get( self.PROCESS['find'][0]['proxy'].content.decode('UTF-8').split('<')[0].split(':')[1].replace('//', '') ) == None and DATABASE[ self.PROCESS['find'][0]['proxy'].content.decode('UTF-8').split('<')[0].split(':')[1].replace('//', '') ]['work'] == False
                            )):
                            
                                DATABASE.update({
                                    self.PROCESS['find'][0]['proxy'].content.decode('UTF-8').split('<')[0].split(':')[1].replace('//', '') : {
                                        'type' : self.PROCESS['find'][0]['proxy'].content.decode('UTF-8').split('<')[0].split(':')[0], 
                                        'port' : self.PROCESS['find'][0]['proxy'].content.decode('UTF-8').split('<')[0].split(':')[2], 
                                        'work' : None
                                    }
                                })
                                print( f'FOUND self.find() gimmeproxy.com { SourceCodeLine().f_lineno }', self.PROCESS['find'][0]['proxy'].content.decode('UTF-8').split('<')[0].split(':')[1].replace('//', '') )
                        except Exception as e:
                            #   print( f'ERROR self.find() gimmeproxy.com { SourceCodeLine().f_lineno }', e )
                            pass

                        try:
                            if re.search(
                                'pubproxy.com', 
                                self.PROCESS['find'][0]['proxy'].request.url
                            ) and not self.PROCESS['find'][0]['proxy'].json().get('data') == None and not self.PROCESS['find'][0]['proxy'].json().get('data') == [] and ((
                                DATABASE.get( self.PROCESS['find'][0]['proxy'].json()['data'][0]['ip'] ) == None
                            ) or (
                                not DATABASE.get( self.PROCESS['find'][0]['proxy'].json()['data'][0]['ip'] ) == None and DATABASE[ self.PROCESS['find'][0]['proxy'].json()['data'][0]['ip'] ]['work'] == False
                            )):
                                DATABASE.update({
                                    self.PROCESS['find'][0]['proxy'].json()['data'][0]['ip'] : {
                                        'type' : self.PROCESS['find'][0]['proxy'].json()['data'][0]['type'], 
                                        'port' : self.PROCESS['find'][0]['proxy'].json()['data'][0]['port'],
                                        'work' : None
                                    }
                                })
                                print( f'FOUND self.find() pubproxy.com { SourceCodeLine().f_lineno }', f'{ self.PROCESS["find"][0]["proxy"].json()["data"][0]["ip"] }:{self.PROCESS["find"][0]["proxy"].json()["data"][0]["port"]}' )
                        except Exception as e:
                            #   print( f'ERROR self.find() pubproxy.com { SourceCodeLine().f_lineno }', e )
                            pass

                        try:
                            if re.search(
                                'proxyflow.io', 
                                self.PROCESS['find'][0]['proxy'].request.url
                            ) and ((
                                DATABASE.get( self.PROCESS['find'][0]['proxy'].json()['ip'] ) == None
                            ) or (
                                not DATABASE.get( self.PROCESS['find'][0]['proxy'].json()['ip'] ) == None and DATABASE[ self.PROCESS['find'][0]['proxy'].json()['ip'] ]['work'] == False
                            )):
                                DATABASE.update({
                                    self.PROCESS['find'][0]['proxy'].json()['ip'] : {
                                        'type' : self.PROCESS['find'][0]['proxy'].json()['protocol'], 
                                        'port' : self.PROCESS['find'][0]['proxy'].json()['port'],
                                        'work' : None
                                    }
                                })
                                print( f'FOUND self.find() proxyflow.io { SourceCodeLine().f_lineno }', f'{ self.PROCESS["find"][0]["proxy"].json()["ip"] }:{self.PROCESS["find"][0]["proxy"].json()["port"]}' )
                        except Exception as e:
                            #   print( f'ERROR self.find() proxyflow.io { SourceCodeLine().f_lineno }', e )
                            pass
                            
                    open(f'{ CONFIGDB["DB"] }', 'w').write(json.dumps(DATABASE, indent = 4))
                    
                    time.sleep(2)
                    continue

                else:
                    
                    time.sleep(20)
                    continue

            except Exception as e:
                
                if re.search('no more proxies left', self.PROCESS['find'][0]['proxy'].content.decode('UTF-8')):
                    #   print( f'ERROR self.find() { SourceCodeLine().f_lineno }', 'NO MORE PROXIES', e )
                    time.sleep(2)
                else:
                    #   print( f'ERROR self.find() { SourceCodeLine().f_lineno }', e )
                    time.sleep(3)
                    
                continue

    def list(
        self, 
        code
    ):

        global DATABASE
        global CONFIGDB
        
        while True:

            try:

                #   print( f'CHECK self.list() { SourceCodeLine().f_lineno } HAVE PROXY', len([ x for x in DATABASE if DATABASE[x]['work'] == True ]), code )

                #   for x in DATABASE:
                for x in [
                    random.choice([ i for i in DATABASE if DATABASE[ i ]['work'] == None ]), 
                    random.choice([ i for i in DATABASE if DATABASE[ i ]['work'] == None ]), 
                    random.choice([ i for i in DATABASE if DATABASE[ i ]['work'] == None ]), 
                    random.choice([ i for i in DATABASE if DATABASE[ i ]['work'] == None ]), 
                    random.choice([ i for i in DATABASE if DATABASE[ i ]['work'] == None ]), 
                    random.choice([ i for i in DATABASE if DATABASE[ i ]['work'] == None ]), 
                    random.choice([ i for i in DATABASE if DATABASE[ i ]['work'] == None ]), 
                    random.choice([ i for i in DATABASE if DATABASE[ i ]['work'] == None ]), 
                    random.choice([ i for i in DATABASE if DATABASE[ i ]['work'] == None ]), 
                    random.choice([ i for i in DATABASE if DATABASE[ i ]['work'] == None ]), 
                    random.choice([ i for i in DATABASE if not DATABASE[ i ]['work'] == True and not DATABASE[ i ]['work'] == None ]), 
                    random.choice([ i for i in DATABASE if not DATABASE[ i ]['work'] == True and not DATABASE[ i ]['work'] == None ]), 
                    random.choice([ i for i in DATABASE if not DATABASE[ i ]['work'] == True and not DATABASE[ i ]['work'] == None ]), 
                    random.choice([ i for i in DATABASE if not DATABASE[ i ]['work'] == True and not DATABASE[ i ]['work'] == None ]), 
                    random.choice([ i for i in DATABASE if not DATABASE[ i ]['work'] == True and not DATABASE[ i ]['work'] == None ]), 
                    random.choice([ i for i in DATABASE if not DATABASE[ i ]['work'] == True and not DATABASE[ i ]['work'] == None ]), 
                    random.choice([ i for i in DATABASE if not DATABASE[ i ]['work'] == True and not DATABASE[ i ]['work'] == None ]), 
                    random.choice([ i for i in DATABASE if not DATABASE[ i ]['work'] == True and not DATABASE[ i ]['work'] == None ]), 
                ]:

                    if code == None and DATABASE[ x ]['work'] == None:
                        print( f'CHECK self.list() { SourceCodeLine().f_lineno } PING NEW', f'{ DATABASE[ x ]["type"] }://{ x }:{ DATABASE[ x ]["port"] }', len([ x for x in DATABASE if DATABASE[x]['work'] == True ]) )
                        DATABASE[ x ]['work'] = self.ping( f'{ DATABASE[ x ]["type"] }://{ x }:{ DATABASE[ x ]["port"] }' )
                        #   open(f'{ CONFIGDB["DB"] }', 'w').write(json.dumps(DATABASE, indent = 4))
                    if code == 429 and DATABASE[ x ]['work'] == 429 and random.randrange(100) >= 25:
                        print( f'CHECK self.list() { SourceCodeLine().f_lineno } PING 429', f'{ DATABASE[ x ]["type"] }://{ x }:{ DATABASE[ x ]["port"] }', len([ x for x in DATABASE if DATABASE[x]['work'] == True ]) )
                        DATABASE[ x ]['work'] = self.ping( f'{ DATABASE[ x ]["type"] }://{ x }:{ DATABASE[ x ]["port"] }' )
                        #   open(f'{ CONFIGDB["DB"] }', 'w').write(json.dumps(DATABASE, indent = 4))
                    if code == False and DATABASE[ x ]['work'] == False and random.randrange(100) >= 50:
                        print( f'CHECK self.list() { SourceCodeLine().f_lineno } PING False', f'{ DATABASE[ x ]["type"] }://{ x }:{ DATABASE[ x ]["port"] }', len([ x for x in DATABASE if DATABASE[x]['work'] == True ]) )
                        DATABASE[ x ]['work'] = self.ping( f'{ DATABASE[ x ]["type"] }://{ x }:{ DATABASE[ x ]["port"] }' )
                        #   open(f'{ CONFIGDB["DB"] }', 'w').write(json.dumps(DATABASE, indent = 4))
                    
            except Exception as e:
                #   print( f'ERROR self.list() { SourceCodeLine().f_lineno }', e )
                pass
            
            time.sleep(2)
            continue
            
    def ping(
        self, 
        data
    ):
        
        global DATABASE
        global CONFIGDB

        try:
            self.PROCESS['ping'][0]['request']     = cloudscraper.create_scraper(
                delay   = 10
            ).post(
                'https://aw-guard.yeomen.ai/platform-guard',
                headers = {
                    'authority'             : 'aw-guard.yeomen.ai',
                    'pragma'                : 'no-cache',
                    'cache-control'         : 'no-cache',
                    'accept'                : '*/*',
                    'sec-gpc'               : '1',
                    'origin'                : 'https://play.alienworlds.io',
                    'referer'               : 'https://play.alienworlds.io/'
                },
                json    = {
                    "account_name"      : 'm.federation', 
                    "actions"           : [{
                        "account"           : "m.federation", 
                        "name"              : "mine", 
                        "authorization"     : [{
                            "actor"             : 'm.federation', 
                            "permission"        : "active"
                        }], 
                        "data"      : {
                            "miner"             : 'm.federation', 
                            "nonce"             : 'f6e49fb54f11d538'
                        }
                    }]
                },
                timeout = 15, 
                proxies = {
                    'http'      : data,
                    'https'     : data
                }
                #   , 
                #   proxies = None
            ); 

            print( f'CHECK self.ping() { SourceCodeLine().f_lineno } { data }', self.PROCESS["ping"][0]["request"] )
            
            if self.PROCESS["ping"][0]["request"].status_code == 403 and not re.search(
                self.PROCESS['ping'][0]['request'].request.headers['User-Agent'], 
                open(f'webagent.not', 'r').read()
            ):
                try:
                    open('webagent.not', 'a').write( self.PROCESS['ping'][0]['request'].request.headers['User-Agent'] + '\n' )
                except:
                    pass
            if self.PROCESS['ping'][0]['request'].status_code == 200 and not re.search(
                self.PROCESS['ping'][0]['request'].request.headers['User-Agent'], 
                open(f'webagent.not', 'r').read()
            ):
                try:
                    open('webagent.yes', 'a').write( self.PROCESS['ping'][0]['request'].request.headers['User-Agent'] + '\n' )
                except:
                    pass

            try:
                self.PROCESS['ping'][0]['not'] = ''.join(open('webagent.not').readlines()[-100:])
                open('webagent.not', 'w').write( self.PROCESS['ping'][0]['not'] )
            except:
                pass
            try:
                self.PROCESS['ping'][0]['yes'] = ''.join(open('webagent.yes').readlines()[-100:])
                open('webagent.yes', 'w').write( self.PROCESS['ping'][0]['yes'] )
            except:
                pass
                
            if self.PROCESS['ping'][0]['request'].status_code == 200:
                return True
            elif self.PROCESS['ping'][0]['request'].status_code == 429:
                return 429
            else:
                return False

        except Exception as e:
            #   print( f'ERROR self.ping() { SourceCodeLine().f_lineno } { data }', str(e)[0:24] )
            return False
        


@app.route('/', methods = ['GET', 'POST'])
def main():
    
    try     :
      ip = requests.get('https://checkip.amazonaws.com').text.strip()
      return {'HOST' : 'POOL CORS SERVICE', 'ip' : ip}, 200
    except  :
      return {'HOST' : 'POOL CORS SERVICE'}, 200

@app.route('/v1/result/<uid>', methods = ['GET', 'POST'])
def v1_result(
    pro = 'https', 
    url = '', 
    uid = ''
):
    try     :
      return json.load(open( f'ticket/{ uid }' ))
    except  :
      return {'HOST' : 'POOL CORS SERVICE'}, 200
    
    
@app.route('/v1/pool/<pro>/<path:url>', methods = ['GET', 'POST'])
def v1_pool(
    pro = 'https', 
    url = ''
):
    global DATABASE
    global CONFIGDB
    
    try:
        if request.json.get('account_name'):
            uid = request.json['account_name']
        else:
            uid = timedate.now().timestamp()
    except:
        uid = timedate.now().timestamp()

    #  return {
    #      "uid" : '', 
    #      "val" : 204, 
    #      'txt' : 'BUSY'
    #  }, 200
        
    if CONFIGDB['WORKED'] > CONFIGDB['THREAD'] or ((
        CONFIGDB['WORKED'] > CONFIGDB['THREAD']
    ) and not (
        random.randrange(1000) >= 900
    )):
        return {
            "uid" : '', 
            "val" : 204, 
            'txt' : 'BUSY'
        }, 200
    else:
        CONFIGDB['WORKED'] += 1
        _thread.start_new_thread(THREAD().cooldown, ())
        
    open(f'ticket/{ uid }', 'w').write(json.dumps({}, indent = 4))
    
    try:
        
        POOL(
            url         = f'{ pro }://{ url }', 
            uid         = uid, 
            method      = request.method, 
            headers     = dict(request.headers), 
            cookies     = dict(request.cookies), 
            form        = dict(request.form), 
            json        = request.json, 
            args        = dict(request.args)
        ).thread()
        
    except Exception as e:
        print( f'ERROR pool() { SourceCodeLine().f_lineno }', e)
        
    return {
        "uid" : uid, 
        "val" : 200, 
        'txt' : 'DONE'
    }, 200

@app.route('/pool/<pro>/<path:url>', methods = ['GET', 'POST'])
def pool(
    pro = 'https', 
    url = ''
):
    
    global DATABASE
    global CONFIGDB
    
    return {
        "uniqid"                : "",
        "account"               : "",
        "enabled"               : False,
        "contract_account"      : "",
        "contract_action"       : "",
        "contract_permission"   : "",
        "buyram_bytes"          : "",
        "account_tag_exists"    : False,
        "stats"                 : {
            "error"                 : None,
            "errorCode"             : None,
            "message"               : "",
            "cosign"                : False,
            "buyram"                : False,
            "cosign_remaining_txs"  : 0
        }
    }, 200
 
#   @app.teardown_request
#   def teardown_request(response):
#   
#       global DATABASE
#       global CONFIGDB
#       
#       if random.randrange(1000) >= 850:
#           CONFIGDB['WORKED'] -= 1
#       if CONFIGDB['WORKED'] <= 0:
#           CONFIGDB['WORKED'] = 0
#       else:
#           CONFIGDB['WORKED'] -= 1

#  if __name__ == "__main__":
    #   from gevent import monkey; monkey.patch_all(  )

_thread.start_new_thread(POOL().find, ())
_thread.start_new_thread(POOL().list, (None,))
_thread.start_new_thread(POOL().list, (429,))
_thread.start_new_thread(POOL().list, (False,))
_thread.start_new_thread(POOL().list, (429,))
_thread.start_new_thread(POOL().list, (False,))
_thread.start_new_thread(POOL().list, (429,))
_thread.start_new_thread(POOL().list, (False,))

if __name__ == "__main__":

    #   print(CONFIGDB)
    #   print(DATABASE)

    ''' # LOADER TEMPLATE
    app.config['TEMPLATES_AUTO_RELOAD']     = True
    '''
    app.config['SECRET_KEY']                = uuid.uuid4().hex
    app.run( host = '0.0.0.0', port = CONFIGDB['PORT'], threaded = True )