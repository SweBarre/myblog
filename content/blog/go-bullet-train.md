Title: Pimp the bash prompt with Go Bullet Train (GBT)
Slug: go-bullet-train
Date: 2019-03-30
Tags: leap15, opensuse, bash, go

Pimp the bash prompt with a fast PS1 builder with a lot of ways for you to customize. Meet the [Go Bullet Train][1]
I've been playing around with [powerline][2] and quite liked it but I was never really completely satisfied. I though the powerline was quite slow, not extremly slow but slow enough for me to get a bit frustraded. I also thought it was a bit of a hassle to update all my devices with new config when I decided to change the prompt.

This is where gbt comes to the rescue, it's fast hand has the possibility to forward prompts to remote servers with a bash implementation calle [gbts][3]

this is how my prompt looks like right now
![alt text][gbt_home]
![alt text][gbt_git_dirty]
![alt text][gbt_git_ahead]
![alt text][gbt_git_clean]
![alt text][gbt_py_venv]
![alt text][gbt_remote_host]


I'm using nerdfont, the 'hack' version of it tp be sepcific. A nerdfont is more or less needed if you want to display OS logo in your bash prompt.

download a nerdfont [https://nerdfonts.com/][4]
unzip it to ~/.fonts and run following command to update font cache
```
fc-cache -fv
```

First make sure you have go installed and fetch the code and install it as your normal user
```
sudo zypper in go1.11
go get -u github.com/jtyr/gbt/cmd/gbt
go install github.com/jtyr/gbt/cmd/gbt
```
**gbt** has a lot of settings, this is my configuration in my .bashrc
```bash
if [[ -f ~/go/bin/gbt ]]; then
    export VIRTUAL_ENV_DISABLE_PROMPT=1
    export PS1='$(~/go/bin/gbt)'
    export GBT_CARS='OS, Git, Dir, PyVirtEnv, Custom1, Custom2, Custom3, Status, Sign'
    export GBT_CAR_OS_NAME='opensuse'
    export GBT_CAR_PYVIRTENV_FORMAT='{{ Icon }}'
    export GBT_CAR_DIR_BG='dark_gray'
    export GBT_CAR_DIR_DEPTH='3'
    export GBT_CAR_STATUS_FORMAT=' {{ Code }} '
    export GBT_CAR_SIGN_USER_TEXT=''
    export GBT_CAR_CUSTOM1_TEXT_TEXT='MyDot: error'
    export GBT_CAR_CUSTOM1_BG='red'
    export GBT_CAR_CUSTOM1_DISPLAY_CMD="/home/jonas/bin/mydot_gbt_status.sh check_error"
    export GBT_CAR_CUSTOM1_TEXT_TEXT='MyDot: err'
    export GBT_CAR_CUSTOM2_BG='green'
    export GBT_CAR_CUSTOM2_FG='black'
    export GBT_CAR_CUSTOM2_TEXT_TEXT='MyDot: commit'
    export GBT_CAR_CUSTOM2_DISPLAY_CMD="/home/jonas/bin/mydot_gbt_status.sh check_status"
    export GBT_CAR_CUSTOM3_TEXT_TEXT='MyDot: push'
    export GBT_CAR_CUSTOM3_BG='green'
    export GBT_CAR_CUSTOM3_FG='black'
    export GBT_CAR_CUSTOM3_DISPLAY_CMD="/home/jonas/bin/mydot_gbt_status.sh check_pull"
    
    #Prompt forward:
    export GBT__HOME="${HOME}/go/src/github.com/jtyr/gbt"
    export GBT__CARS_REMOTE='OS, Hostname, Git, Dir, Status, Sign'
    export GBT__THEME_SSH="${HOME}/.gbts_theme.sh"
    source  ~/go/src/github.com/jtyr/gbt/sources/gbts/cmd/local.sh
    alias ssh='gbt_ssh'
fi
```

the prompt forward theme looks like this
```bash
export GBT_CARS="${GBT__THEME_REMOTE_CARS:=OS, Hostname, Git, Dir, Status, Sign}"
export GBT_CAR_DIR_BG='dark_gray'
export GBT_CAR_DIR_DEPTH='3'
export GBT_CAR_SIGN_USER_TEXT=''
export GBT_CAR_STATUS_FORMAT=' {{ Code }} '
export GBT_CAR_HOSTNAME_ADMIN_FG='light_red'
export GBT_CAR_HOSTNAME_USER_FG='green'
export GBT_CAR_HOSTNAME_USER_BG='dark_gray'
export GBT_CAR_HOSTNAME_HOST_FG='light_green'
export GBT_CAR_HOSTNAME_HOST_BG='dark_gray'
export GBT_CAR_HOSTNAME_HOST_FM='bold'
```

I do have som issues that I've not figured out yet.

-	<s>unable to force pseudo-terminal allocation with the `gbt_ssh` alias</s> **fixed in commit [c6fd3ca][5]**
-	<s>I'm unable to remove the `GBT_CAR_SIGN_USER_TEXT` with prompt forward</s> **fixed in commit [c02a775][6]**

But so far I can live with thouse issues

[gbt_home]: {static}/images/gbt_home.png "Home directory"
[gbt_git_dirty]: {static}/images/gbt_git_dirty.png "Dirty git repo"
[gbt_git_ahead]: {static}/images/gbt_git_ahead.png "Git repo ahead"
[gbt_git_clean]: {static}/images/gbt_git_clean.png "Git repo clean"
[gbt_py_venv]: {static}/images/gbt_py_venv.png "Python Virtual Env"
[gbt_remote_host]: {static}/images/gbt_remote_host.png "Remote host" 


[1]: https://github.com/jtyr/gbt
[2]: https://github.com/powerline/powerline
[3]: https://github.com/jtyr/gbt/blob/master/sources/gbts/README.md
[4]: https://nerdfonts.com/
[5]: https://github.com/jtyr/gbt/commit/c6fd3cac1d1ded90f8e60cd243b48b7dc0037c0b
[6]: https://github.com/jtyr/gbt/commit/c02a7755e8eaeffeb61597bc3d763251f3c231b4
