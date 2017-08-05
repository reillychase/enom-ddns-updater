# enom_ddns_updater
Dynamically updates your enom DNS hosted record


# Instructions
1. Login to Enom
2. Go to Domains
3. Select your domain (must use enom hosted DNS)
4. Go to Domain Settings
5. Set Domain password
6. Update script variables at top -- 
7. set ip_check_url to a known good website which returns only your public IP address
8. set ip_text_file location to location of file on update running server, this is where ip will be stored for checking
9. set domain to your enom domain
10. set password to domain password set previously in enom dashboard

# Warning
This script currently has SSL verification disabled, so passwords are transmitted encrypted, however the SSL is vulnerable to a man in the middle attack if someone were to intercept the request and serve it a fake SSL. I have sent an email to enom support to fix the SSL errors, hopefully they will do that soon and I will update the repo with SSL verification again.

# Credits
update_enom.py by: Sean Schertell, DataFly.Net
http://secure.datafly.net/articles/update_enom.php
