
    
    
    
    
    
    
    
    
    
    

    #   return {
    #       "uniqid"                : "",
    #       "account"               : "",
    #       "enabled"               : False,
    #       "contract_account"      : "",
    #       "contract_action"       : "",
    #       "contract_permission"   : "",
    #       "buyram_bytes"          : "",
    #       "account_tag_exists"    : False,
    #       "stats"                 : {
    #           "error"                 : None,
    #           "errorCode"             : None,
    #           "message"               : "",
    #           "cosign"                : False,
    #           "buyram"                : False,
    #           "cosign_remaining_txs"  : 0
    #       }
    #   }, 200
    #   return {
    #       "uniqid"                : timedate.now().timestamp()
    #   }, 200
    #   if CONFIGDB['WORKED'] > CONFIGDB['THREAD']:
    #       return {
    #           "uniqid"                : "",
    #           "account"               : "",
    #           "enabled"               : False,
    #           "contract_account"      : "",
    #           "contract_action"       : "",
    #           "contract_permission"   : "",
    #           "buyram_bytes"          : "",
    #           "account_tag_exists"    : False,
    #           "stats"                 : {
    #               "error"                 : None,
    #               "errorCode"             : None,
    #               "message"               : "",
    #               "cosign"                : False,
    #               "buyram"                : False,
    #               "cosign_remaining_txs"  : 0
    #           }
    #       }, 200
    #   else:
    #       
    #       CONFIGDB['WORKED'] += 1
    #       
    #       try:
    #           return Response(getattr(
    #               POOL(
    #                   url     = f'{ pro }://{ url }', 
    #                   req     = request, 
    #                   form    = request.form, 
    #                   json    = request.json, 
    #                   args    = request.args
    #               ), 
    #               request.method.lower()
    #           )()) 
    #       except Exception as e:
    #           print( f'ERROR pool() { SourceCodeLine().f_lineno }', e)
    #           return {
    #               'code'  : 204, 
    #               'text'  : f'INCORRECT REQUEST {e}'
    #           }, 200













                        #   self.PROCESS['find'][0]['proxy'] = cloudscraper.create_scraper(
                        #       delay   = 8
                        #   ).get(
                        #       random.choice([
                        #           'https://cors.bridged.cc/https://gimmeproxy.com/api/getProxy?curl=true&supportsHttps=true&referer=true&post=true'
                        #       ] * 0 + [
                        #           'http://pubproxy.com/api/proxy?format=json&https=true&post=true&user_agent=true&referer=true'
                        #       ] * 1), 
                        #       headers = {
                        #           'x-requested-with'      : 'XMLHttpRequest',
                        #           'x-cors-grida-api-key'  : '61dbebf9-36c6-45c6-909e-323209a8116d',
                        #       },
                        #       timeout = 8
                        #   )
                        #   cloudscraper.create_scraper(
                        #       delay   = 8
                        #   ).get(
                        #       random.choice([
                        #           'https://cors.bridged.cc/https://www.proxyscan.io/api/proxy?format=json&https=true&post=true&user_agent=true&referer=true'
                        #       ] * 0 + [
                        #           'https://cors.bridged.cc/http://pubproxy.com/api/proxy?format=json&https=true&post=true&user_agent=true&referer=true'
                        #       ] * 1), 
                        #       headers = {
                        #           'x-requested-with'      : 'XMLHttpRequest',
                        #           'x-cors-grida-api-key'  : '61dbebf9-36c6-45c6-909e-323209a8116d',
                        #       },
                        #       timeout = 16
                        #   )

                        #   print( f'CHECK self.find() { SourceCodeLine().f_lineno }', self.PROCESS['find'][0]['proxy'] )

                        #   if (
                        #       re.findall('{|}', str(self.PROCESS['find'][0]['proxy'].content)) and not DATABASE.get( self.PROCESS['find'][0]['proxy'].json()['data'][0]['ip'] )
                        #   ) or ((
                        #       re.findall('{|}', str(self.PROCESS['find'][0]['proxy'].content)) and DATABASE.get( self.PROCESS['find'][0]['proxy'].json()['data'][0]['ip'] )
                        #   ) and (
                        #       DATABASE[ self.PROCESS['find'][0]['proxy'].json()['data'][0]['ip'] ]['work'] == False
                        #   )):
                        #       DATABASE.update({
                        #           self.PROCESS['find'][0]['proxy'].json()['data'][0]['ip'] : {
                        #               'type' : self.PROCESS['find'][0]['proxy'].json()['data'][0]['type'], 
                        #               'port' : self.PROCESS['find'][0]['proxy'].json()['data'][0]['port'], 
                        #               'work' : None
                        #           } 
                    #       })  
                        #       print( f'FOUND self.find() { SourceCodeLine().f_lineno }', self.PROCESS['find'][0]['proxy'], self.PROCESS['find'][0]['proxy'].json()['data'][0]['ip'] )
    