Title: Pimp the bash prompt with Go Bullet Train (GBT)
Slug: go-bullet-train
Date: 2019-03-30
Tags: leap15, opensuse, bash, go
download a nerdfont https://nerdfonts.com/
unzip it to ~/.fonts
run fllowing command to update
fc-cache -fv


Install
  846  sudo zypper in go1.11
  847  go get -u github.com/jtyr/gbt/cmd/gbt
  848  ll
  849  go install github.com/jtyr/gbt/cmd/gbt

export GBT_CARS='OS, Git, Dir, Status, Sign'
export GBT_CAR_DIR_BG='dark_gray'
export GBT_CAR_OS_NAME='opensuse'
export GBT_CAR_DIR_DEPTH='3'
export GBT_CAR_SIGN_USER_TEXT=''
export GBT_CAR_STATUS_FORMAT=' {{ Code }} '






Prompt forward:
export GBT__HOME="${HOME}/go/src/github.com/jtyr/gbt"
source  ~/go/src/github.com/jtyr/gbt/sources/gbts/cmd/local.sh

alias ssh='gbt_ssh'

