Title: Local DOH stub
Slug: local-doh-proxy
Date: 2019-03-27
Tags: leap15, doh, opensuse, systemd, bash
Summary: To really get the full use of the DOH I created a small systemd unit file on my client so all applications will use my DOH server and not just firefox. 

To really get the full use of the [DOH][1] I created a small systemd unit file on my client so all applications will use my DOH server and not just firefox.

Because the local DOH proxy on my client machine will be listening on port 53 (dns) I will have to run this as root (I guess there are some systemd magic that would be able ti fix that but I'm not investigating this at them moment).

First off we need to install the doh-proxy on the client system
```
sudo pip3 install doh-proxy
```

Then create a systemd unit file for our service.
Before the service start we inject a nameserver in /etc/resolv.conf that points to 127.0.0.1 as the first nameserver.
After that we launch the  doh-stub and point it to your doh endpoint (remember to change to domain to fit your setup.
When the service is stopped we remove the nameserver we injected.
```
cat << EOF | sudo tee /etc/systemd/system/local-doh-proxy.service
[Unit]
Description=Local DOH Proxy
After=syslog.target network.target

[Service]
Type=simple
ExecStartPre=/bin/bash -c "/usr/bin/sed -i '0,/^nameserver .*/ s/^nameserver .*/nameserver 127.0.0.1\\n&/' /etc/resolv.conf"
ExecStart=/usr/bin/doh-stub --domain www.example.com --listen-address 127.0.0.1
ExecStopPost=/bin/bash -c "/usr/bin/sed -i '/^nameserver 127.0.0.1$/d' /etc/resolv.conf"
Restart=no

[Install]
WantedBy=multi-user.target
```

I don't want this to be the default way to do name resolution on my system so I don't enable it, but we still have to do a daemon-reload so systemd picks up the changes.
```
sudo systemctl daemon-reload
```

now when ever I want to utilize DOH on my client machine I just have to start the doh-stub by running
```
sudo systemctl status local-doh-proxy
```

just to simplefy things I've createde a bash function called doh
```bash
function doh()
{
    local options
    options=(start stop restart status)
    if [[ ! " ${options[@]} " =~ " ${1} " ]]; then
        echo "wrong option, valid: ${options[@]}"
        return
    fi
    sudo systemctl "$1" local-doh-proxy
}
```



[1]: playing-with-doh.html
