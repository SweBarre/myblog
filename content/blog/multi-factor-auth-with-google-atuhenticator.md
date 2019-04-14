Title: Multi-Factor Auth with google-atuhenticator
Slug:  multi-factor-auth-with-google-atuhenticator
Date:  2019-04-12 17:33:40
Tags:  leap15, google, ssh

To harden the security on my SSH-server at home I enabled Multi-Factor Authentication with Google Authenticator

**make sure you don't lock yourself out of the system if you do this through an SSH connection**
```
sudo zypper in google-authenticator-libpam
```

add the pam_google_authenticator.so to the /etc/pam.d/sshd
```
#%PAM-1.0
auth        required    pam_google_authenticator.so nullok
auth        requisite   pam_nologin.so
auth        include     common-auth
account     requisite   pam_nologin.so
account     include     common-account
password    include     common-password
session     required    pam_loginuid.so
session     include     common-session
session     optional    pam_lastlog.so   silent noupdate showfailed
session     optional    pam_keyinit.so   force revoke
```

as your user, run the google-authenticator
```
google-authenticator \
  --time-based \
  --disallow-reuse \
  --qr-mode=UTF8 \
  --window-size=3 \
  --rate-limit=3 \
  --rate-time=30 \
  --force
```

Add the the secret key (first line in ~/.google_authenticator) to your Google Authenticator app on your phone

make sure ChallengeResponseAuthentication is set to yes in /etc/ssh/sshd_config
```
ChallengeResponseAuthentication yes
```

restart the ssh-server
```
sudo systemctl restart sshd
```

Now, you should just be automaticly logged in if you have configured ssh-keys, if not you'll be prompted for a verification key before entering your password
