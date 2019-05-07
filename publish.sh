#!/bin/bash
./add_matomo.sh
make publish
rsync -rave ssh output/ web:/srv/www/rre.nu/
