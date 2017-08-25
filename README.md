# Enom DDNS Updaer
Dynamically updates your enom DNS hosted record

## Instructions
1. Login to Enom
2. Go to Domains
3. Select your domain (must use enom hosted DNS)
4. Go to Domain Settings
5. Set Domain password
6. Customize the scrip variables: set ip_check_url to a known good website which returns only your public IP address
7. Set domain to your enom domain
8. Set password to domain password set previously in enom dashboard

## Credits
Modified from
update_enom.py by: Sean Schertell, DataFly.Net
http://secure.datafly.net/articles/update_enom.php

## Revisions from original script
1. The original script saved the current IP to a text file and only updated DNS if the newly checked IP didn't match. I removed that logic to instead resolve the domain name and compare that to the newly checked IP. That way if for some reason the DNS gets manually messed up it will still be fixed by the updater rather than having to wait until an IP change.


