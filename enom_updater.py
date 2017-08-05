#!/usr/local/bin/python

##############################################
# update_enom.py by: Sean Schertell, DataFly.Net, rchase
# Revised by rchase 8/5/2017: 
# Temporarily removed SSL verification because enom SSL has errors
# Added to github repo at https://github.com/reillychase/enom_ddns_updater with instructions
# Modified functions that saved/retrieved current IP to text file, replaced with DNS check to see current IP
# of host that way it will still update even if the record is changed for some other reason
# ------------------------
# A simple python script to update your dynamic DNS IP for domains registered with Enom.
# 
# Requirements:
# - You have a domain registered with Enom, nameservers are set to Enom's, and you've set a domain password
# - Your client machine runs python
# - You know how to configure a cron job to periodically run this script (every 5 mins recommended)
#
# Cron example to run every 5 minutes:
# */5 * * * * /usr/local/bin/update_enom.py

##############################################
# Configure
##############################################

ip_check_url = 'http://icanhazip.com' # URL which returns current IP as text only
domain       = 'example.com'                         # Enom registered domain to be altered
password     = 'secret'                              # Domain password

##############################################

import urllib2, os, ssl, socket

def read_url(url):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return urllib2.urlopen(url, context=ctx).read()

def parse_enom_response(enom_response):
    enom_response_dict = {}
    for param in  enom_response.split('\n'):
        if '=' in param:
            try:
                key, val = param.split('=')
                enom_response_dict[key] = val.strip()
            except: pass
    return enom_response_dict

def update_enom():    

    # Compare our current IP to the domain's current IP
    recent_ip = socket.gethostbyname(domain)
    current_ip = read_url(ip_check_url)

    # Do they match?
    if recent_ip == current_ip:
        return # IP address has not changed since last update

    # No match, so let's try to update Enom
    settings = {'domain': domain, 'password': password, 'current_ip': current_ip}
    enom_update_url = 'https://dynamic.name-services.com/interface.asp?command=setdnshost&zone=%(domain)s&domainpassword=%(password)s&address=%(current_ip)s' % settings
    enom_response = read_url(enom_update_url)

    # Any errors?
    response_vals = parse_enom_response(enom_response)

    if not response_vals['ErrCount'] == '0':    
        raise Exception('*** FAILED TO UPDATE! Here is the response from Enom:\n' + enom_response)

    return    
##############################################

update_enom()
