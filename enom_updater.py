#!/usr/local/bin/python

##############################################
# update_enom.py by: Sean Schertell, DataFly.Net
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
ip_text_file = '/usr/local/etc/update_enom.txt'      # Text file to store recent ip file
domain       = 'example.com'                         # Enom registered domain to be altered
password     = 'secret'                              # Domain password

##############################################

import urllib2, os, ssl

def read_url(url):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE
    return urllib2.urlopen(url, context=ctx).read()

def read_file(path):
    return open(path, 'r').read()

def parse_enom_response(enom_response):
    enom_response_dict = {}
    for param in  enom_response.split('\n'):
        if '=' in param:
            try:
                key, val = param.split('=')
                enom_response_dict[key] = val.strip()
            except: pass
    return enom_response_dict

def save_new_ip(current_ip):
    return open(ip_text_file, 'w').write(current_ip)

def update_enom():    
    # First, ensure that the ip_text_file exists
    if not os.path.exists(ip_text_file):
        open(ip_text_file, 'w').close() 

    # Compare our recently saved IP to our current real IP
    recent_ip = read_file(ip_text_file)
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

    # Okay then, lets save the new ip
    save_new_ip(current_ip)
    return    
##############################################

update_enom()
