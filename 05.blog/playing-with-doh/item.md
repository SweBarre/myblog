---
publish_date: 03/26/2019 20:00
---
I decided to play a bit with [DNS Over HTTPS][1] (DOH) and get access to my [Pi-Hole][2] at home when I'm out traveling. DOH is a protocol that bypass the native resolver and do DNS-query over HTTPS to a dedicated DOH server for resolving names.

When writing this note I'm using [openSUSE Leap 15][3] but it should be relativly easy to convert the steps in any systemd enabled linux. Although DOH specifies that it must run HTTPS there's a HTTP proxy available that I will use and serve behind a NGINX proxy and let [NGINX][6], [Let's Encrypt][5] and [Certbot][4] handle the SSL

in this example I'll be using some addresses and dns-names that you have to change to fit your environment.
1. upstream-resolver

   I'm using my Pi-Hole as upstream resolver and that's located on my internal network at home (in this example the IP for that Pi-Hole server is 10.10.10.10)
2. web site that hosts the doh

   The website that hosts the doh is www.example.com and the default uri for the doh is /dns-query

#Installing the DOH-Proxy
This installs the doh-proxy and creates a systemd service that listens on loopback (127.0.0.1) on port 9090. It will forward the dns query to the _--upstream-resolver_ dns (10.10.10.10 in this example).
##Creating the DOH user and install doh-httpproxy
Create a user group that should run the DOH proxy
```
groupadd doh
useradd -c "DOH Proxy user" -g doh -m doh
```

Switch to that user and install doh-proxy in a virtual environment and then set shell for doh user to /sbin/nologin
```
su - doh
python3 -m venv doh-proxy
cd doh-proxy/
source bin/activate
pip install doh-proxy
exit
usermod -s /sbin/nologin doh
```

##Creating the doh-httpproxy systemd unit file
Create the systemd unit file for the doh-httpproxy
```
cat <<EOF > /etc/systemd/system/doh-httpproxy.service
[Unit]
Description=DOH HTTP Proxy
After=syslog.target network.target
Before=nginx.target

[Service]
Type=simple
ExecStart=/home/doh/doh-proxy/bin/doh-httpproxy --upstream-resolver 10.10.10.10 --level DEBUG --listen-address=127.0.0.1 --port 9090
Restart=always
User=doh
Group=doh
PrivateTmp=yes


[Install]
WantedBy=multi-user.target
EOF
```
run the deamon-reload to pickup the changed configuratio and enable and start the service
```
systemctl daemon-reload
systemctl enable doh-httpproxy
systemctl start doh-httpproxy
```
check if the doh-httpproxy is running and that nothing has logged as error in the log
```
systemctl status doh-httpproxy
journalctl --unit doh-httpproxy
```

#Installing and configure NGINX and certbot
```
zypper in nginx certbot
```
enable and start the nginx web server
```
systemctl enable nginx
systemctl start nginx
```

Create a Let's Encrypt certificate for your domain and let certbot create a configuration to redirect all http to https
```
certbot --nginx -d www.example.com
```

Configure the nginx configuration and add the following block just before the **server {** definition
```nginx
upstream dohproxy_backend {
        server 127.0.0.1:9090;
}
```
and in the **server {..}** tag add the following
```nginx
       location /dns-query {
	       if ( $request_method !~ ^(GET|POST|HEAD)$ ) {
                   return 501;
               }
               proxy_set_header Host $http_host;
               proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
               proxy_redirect off;
               proxy_buffering off;
               proxy_pass http://dohproxy_backend/dns-query;
       }
```
and then restart the nginx
```
systemctl restart nginx
```

#Testing the installation
A doh client was installed with the doh-proxy and you could test with that tool
```
/home/doh/doh-proxy/bin/doh-client --domain www.example.com --qtype A --qname google.se
```
You should get a DOH response printed in the terminal.

## Firefox
Support for DOH in Firefox was relesed in version 62 and is disabled by default. To enable it you have to configure it in the about:config section, just enter *network.trr* in the search box and hit enter.
There's two settings you have to configure to use your new DOH setup.
1. **network.trr.uri**

   This has to point to a https server, http will simply be ignored
   enter the URL to your doh: https://www.example.com/dns-query
2. **network.trr.mode**

   The default is 0 and disables the use of doh. Change it to **2**
   This means that it will resolve using DOH but if it fails it will fallback to normal resolving. You can read more about the setting in firefox [here](https://daniel.haxx.se/blog/2018/06/03/inside-firefoxs-doh-engine/)




#references
* Daniel Stenberg: [Inside firefoxs DOH engine](https://daniel.haxx.se/blog/2018/06/03/inside-firefoxs-doh-engine/)
* Lennart Poettring: [systemd for Administrators, Part XII](http://0pointer.de/blog/projects/security.html)

[1]: https://tools.ietf.org/html/draft-ietf-doh-dns-over-https-09
[2]: https://pi-hole.net/
[3]: https://www.opensuse.org/#Leap
[4]: https://certbot.eff.org/
[5]: https://letsencrypt.org/
[6]: https://www.nginx.com/
