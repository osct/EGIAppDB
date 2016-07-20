#!/usr/bin/env python

#
#  Copyright 2016 EGI Foundation
# 
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
#
#/

import httplib
import xmltodict

__author__    = "Giuseppe LA ROCCA"
__email__     = "giuseppe.larocca@egi.eu"
__version__   = "$Revision: 0.0.4"
__date__      = "$Date: 13/07/2016 16:21:19"
__copyright__ = "Copyright (c) 2016 EGI Foundation"
__license__   = "Apache Licence v2.0"

apikey = "XXXXXXXXXXXXX-XXXX-XXXX-XXXXXXXXXXXX" # <== Change here!
vo = "training.egi.eu"

def appdb_call(c):
        global apikey
        conn  =  httplib.HTTPSConnection('appdb.egi.eu')
        conn.request("GET", c)
        data = conn.getresponse().read()
        conn.close()
        data.replace('\n','')
        return xmltodict.parse(data)


def main():

        print " ~ Listing providers subscribed the [%s] VO" %vo
        data = appdb_call('/rest/1.0/sites?flt=%%2B%%3Dvo.name:%s&%%2B%%3Dsite.supports:1' %vo)

	for site in data['appdb:appdb']['appdb:site']:
                if  type(site['site:service']) == type([]):
                    for service in site['site:service']:
                       try:
			 url = ("http://appdb.egi.eu/rest/1.0/va_providers/%s" %service['@id'])
                         print "\n- %s [%s] \n\t--> Sitename: %s \
					    \n\t--> Hostname: %s \
					    \n\t--> Status: %s \
					    \n\t--> URL: %s" \
				% (site['@name'],
				   service['@id'],
				   site['site:officialname'], 
				   service['@host'],  
				   site['@status'], 
				   url)

			
			 print "\n ~ Getting published resource_tpl\n"
        		 va_data = appdb_call('/rest/1.0/va_providers/%s' %service['@id'])
			 for resource_tpl in va_data['appdb:appdb']['virtualization:provider']['provider:template']:
			 	print "\t%s" %resource_tpl['provider_template:resource_id']
			 
 			 print "\n ~ Getting published os_tpl"
			 for os_tpl in va_data['appdb:appdb']['virtualization:provider']['provider:image']:
			 	try:
					if vo in os_tpl['@voname']:
					 	print "\n\t - Name = %s [v%s] " %(os_tpl['@appname'], os_tpl['@vmiversion'])
					 	print "\t - OCCI ID = %s" %os_tpl['@va_provider_image_id']
			 			print "\t - URI = %s" %os_tpl['@mp_uri']
				except:
					print ""

                       except:
                       	print ""
	
                else:
			url = ("http://appdb.egi.eu/rest/1.0/va_providers/%s" %site['site:service']['@id'])
                    	print "\n- %s [%s] \n\t--> Sitename: %s \
				           \n\t--> Hostname: %s \
				           \n\t--> Status: %s \
					   \n\t--> URL: %s" \
				% (site['@name'],
				   site['site:service']['@id'], 
				   site['site:officialname'], 
				   site['site:service']['@host'], 
				   site['@status'], 
				   url)
			 
			print "\n ~ Getting published resource_tpl\n"
        		va_data = appdb_call('/rest/1.0/va_providers/%s' %site['site:service']['@id'])

			for resource_tpl in va_data['appdb:appdb']['virtualization:provider']['provider:template']:
                        	print "\t%s" %resource_tpl['provider_template:resource_id']

			print "\n ~ Getting published os_tpl"
                        for os_tpl in va_data['appdb:appdb']['virtualization:provider']['provider:image']:
				try:
					if vo in os_tpl['@voname']:
	                        		print "\n\t - Name = %s [v%s] " %(os_tpl['@appname'], os_tpl['@vmiversion'])
        	                        	print "\t - OCCI ID = %s" %os_tpl['@va_provider_image_id']
                	                	print "\t - URI = %s" %os_tpl['@mp_uri']
				except:
					print ""

	print
	
if __name__ == "__main__":
        main()
