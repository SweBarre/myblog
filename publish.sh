#!/bin/bash
./add_matomo.sh
make publish
rsync -r -a -v -e ssh --delete output/ web:/srv/www/rre.nu/
