##Required packages
* nginx
* Python3
* Git
* pip
* virtualenv
* uwsgi
* flask
* pytoml
* wtforms

##Navod
http://vladikk.com/2013/09/12/serving-flask-with-nginx-on-ubuntu/
Https
* https://www.digitalocean.com/community/tutorials/how-to-secure-nginx-with-let-s-encrypt-on-ubuntu-16-04
* https://www.digitalocean.com/community/tutorials/how-to-create-an-ssl-certificate-on-nginx-for-ubuntu-14-04


##Sec testy
https://securityheaders.io/
https://www.ssllabs.com/ssltest/

## Nginx vritual host config
upravit cestu k aplikaci v  "generator.cupkyvodky.cz" a pridat do /etc/nginx/sites-available
udelat link do /etc/nginx/sites-enable 

## Starting services
zatim bez upstart skriptu
na to chlast-gen-wsgi.ini je pripravenej template v /deploy
```
$ sudo service nginx reload
$ uwsgi --ini chlast-gen-wsgi.ini
```    

