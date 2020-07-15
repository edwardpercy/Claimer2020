import atexit
import datetime
import importlib
import itertools
import json
import logging
import os
import pickle
import random
import re
import secrets
import signal
import sqlite3
import sys
import time
import string
#import eventlet 



from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QIcon
from requests.exceptions import Timeout
required_modules = ["requests","fake_useragent"]

for modname in required_modules:
    try:
        # try to import the module normally and put it in globals
        globals()[modname] = importlib.import_module(modname)
    except ImportError as e:
        if modname != "fake_useragent":
            print(
                f"Failed to load module {modname}. Make sure you have installed correctly all dependencies."
            )
            if modname == "instaloader":
                print(
                    f"If instaloader keeps failing and you are running this script on a Raspberry, please visit this project's Wiki on GitHub (https://github.com/instabot-py/instabot.py/wiki) for more information."
                )
            quit()
from requests.packages.urllib3.exceptions import InsecureRequestWarning

#from instabot import *
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class InstaChecker:   
    s = requests.Session()
    def __init__(self,proxiesL):
        self.proxiesL2 = proxiesL
        self.names = ['bob','harry','harrsis','timford','timmy','charlie','arthur','joe','anne','craig']


        self.emailsChoice = ['technicaldrawde2@gmail.com',
                        'harrison45222@gmail.com',
                        'edward64.kool@gmail.com',
                        'finding83yes@gmail.com',
                        'ifnoyes73@gmail.com',
                        'limnuxrules93@gmail.com',
                        'davidtomlinson382@gmail.com',
                        ]
        # self.list_of_ua = [
        #     "Mozilla/5.0 (Linux; U; Android 1.5; de-de; HTC Magic Build/CRB17) AppleWebKit/528.5+ (KHTML, like Gecko) Version/3.1.2 Mobile Safari/525.20.1",
        #     "Mozilla/5.0 (Linux; U; Android 2.1-update1; en-au; HTC_Desire_A8183 V1.16.841.1 Build/ERE27) AppleWebKit/530.17 (KHTML, like Gecko) Version/4.0 Mobile Safari/530.17",
        #     "Mozilla/5.0 (Linux; U; Android 4.2; en-us; Nexus 10 Build/JVP15I) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30",
        #     "Mozilla/5.0 (Linux; U; Android-4.0.3; en-us; Galaxy Nexus Build/IML74K) AppleWebKit/535.7 (KHTML, like Gecko) CrMo/16.0.912.75 Mobile Safari/535.7",
        #     "Mozilla/5.0 (Linux; U; Android-4.0.3; en-us; Xoom Build/IML77) AppleWebKit/535.7 (KHTML, like Gecko) CrMo/16.0.912.75 Safari/535.7",
        #     "Mozilla/5.0 (Linux; Android 4.0.4; SGH-I777 Build/Task650 & Ktoonsez AOKP) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19",
        #     "Mozilla/5.0 (Linux; Android 4.1; Galaxy Nexus Build/JRN84D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19",
        #     ]
        self.list_of_ua = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)',
            'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729)',
            'Mozilla/5.0 (Linux; Android 7.0; HTC 10 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.83 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; U; Android-4.0.3; en-us; Galaxy Nexus Build/IML74K) AppleWebKit/535.7 (KHTML, like Gecko) CrMo/16.0.912.75 Mobile Safari/535.7',
            'Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-N910F Build/MMB29M) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/4.0 Chrome/44.0.2403.133 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 5.0; SAMSUNG SM-N900 Build/LRX21V) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/2.1 Chrome/34.0.1847.76 Mobile Safari/537.36',
            'Mozilla/5.0 (Linux; Android 6.0.1; SAMSUNG SM-G570Y Build/MMB29K) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/4.0 Chrome/44.0.2403.133 Mobile Safari/537.36',
            'Mozilla/5.0 (Windows NT 5.1; rv:11.0) Gecko Firefox/11.0 (via ggpht.com GoogleImageProxy)',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 1.1.4322)',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.157 Safari/537.36',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1)',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko',
            'Mozilla/5.0 (Windows NT 5.1; rv:7.0.1) Gecko/20100101 Firefox/7.0.1',
            'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1)',
        ]
 
   

    def check(self, check_name, Tproxy):
      
       # proxies = {"http": f"https://{Tproxy}", "https": f"https://{Tproxy}"}
        proxies = {"https": f"https://{Tproxy}"}
        self.s.proxies.update(proxies)
        #proxies = {"http": "https://1111ambush:Scraping67**@[2a0b:4040:95a:e57f:6b43:524c:95b5:724b]", "https": "https://1111ambush:Scraping67**@[2a0b:4040:95a:e57f:6b43:524c:95b5:724b]"}
        
        #proxies = {"https": f"https://{Tproxy.strip()}"}
    
       
        # head = {"method": "POST", "X-CSRFToken":"missing",
        #             "Referer": "https://www.instagram.com/accounts/emailsignup/",
        #             "X-Requested-With":"XMLHttpRequest",
        #             "path":"/accounts/web_create_ajax/attempt/",
        #             "accept": "*/*", "ContentType": "application/x-www-form-urlencoded",
        #             "mid":cookie,"csrftoken":"missing","rur":"FTW","user-agent":random.choice(self.list_of_ua)}
                    
        self.s.headers.update(
            {"method": "POST", "X-CSRFToken":"missing",
                    "Referer": "https://www.instagram.com/accounts/emailsignup/",
                    "X-Requested-With":"XMLHttpRequest",
                    "path":"/accounts/web_create_ajax/attempt/",
                    "accept": "*/*", "ContentType": "application/x-www-form-urlencoded",
                    "mid":secrets.token_hex(8)*2,"csrftoken":"missing","rur":"FTW","user-agent":random.choice(self.list_of_ua)}
        )

     
        self.edit_post = {
            "email": random.choice(self.emailsChoice),
            "enc_password": f"#PWD_INSTAGRAM_BROWSER:0:{time.time()}:D638*fjn4j3w",
            "username": check_name,
            "first_name": random.choice(self.names),
            "opt_into_one_tap": "false",
        }


        #time.sleep(random.randint(self.MIN_DELAY,self.MAX_DELAY))
        try:   
       
            #with eventlet.Timeout(3):
            #prev = time.perf_counter()
            login = self.s.post(
                    "https://www.instagram.com/accounts/web_create_ajax/attempt/", data=self.edit_post, allow_redirects=True, timeout = 10
                ) 
            # login = requests.post(
            #     "https://www.instagram.com/accounts/web_create_ajax/attempt/", data=edit_post, allow_redirects=False, timeout = 40, headers = head, proxies = proxies, verify = False
            # )   
            #print(time.perf_counter() - prev)
            statusCode = login.status_code
            if (statusCode == 200):

                loginResponse = login.json()
                if loginResponse.get("dryrun_passed") == True: #Claimable
                    print("Claimable")
                    print(login.text)
                    
                    login.close()
                    return 1
                elif loginResponse.get("dryrun_passed") == False: #Taken
                    login.close()
                    return 0
                else:
                    print(login.text)
                    login.close()
                    return 3

            elif (statusCode == 429): 
                print("Response Status: ", statusCode)
                login.close()
                return 3
            elif (statusCode == 400):
                    
                print("Response Status: ", statusCode)
                login.close()
                return 2
            elif (statusCode == 500 or statusCode == 501 or statusCode == 502 or statusCode == 503 or statusCode == 560):
                login.close()
                return 6
            else:
                print("Response Status: ", statusCode)
                login.close()
                return 5
        except:
            
            return 4
            
       
            

