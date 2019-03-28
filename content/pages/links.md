Title: Links
Slug: links
Date: 2019-03-29

A collection of useful links I've saved and used to setup my computer

#Password Management with Vim and GnuPG

**[link](https://pig-monkey.com/2013/04/password-management-vim-gnupg/)**

Clever setup to manage password and other sensitive information with vim en GnuPG.
I'm using my bash function though, not using git. I'm saving my [Nextcloud](https://nextcloud.com/) to save my password files, I also have a tab completion to the pw function
```bash
function pw(){
    FILE="$1"

    [[ -z "$PWHOME" ]] && printf "\$PWHOME not set\n"  && return

    [[ -z "$FILE" ]] && FILE="web.gpg"

    if [[ ! "${FILE: -4}" == ".gpg" ]];then
        FILE="${FILE}.gpg"
    fi
    cd "$PWHOME"
    vi "$FILE"

    cd "$OLDPWD"
}

_pw_completion()
{
    local cur prev suggestions
    [[ -z "$PWHOME" ]] && return
    cur="${COMP_WORDS[COMP_CWORD]}"
    prev="${COMP_WORDS[COMP_CWORD-1]}"
    cd "$PWHOME"
    suggestions="$(ls *.gpg)"
    cd "$OLDPWD"
    if [[ "$prev" != "pw" ]];then
        COMPREPLY=()
    else
        COMPREPLY=( $(compgen -W "${suggestions}" -- ${cur}) )
    fi
}
complete -F _pw_completion pw
```
