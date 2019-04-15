#!/bin/bash
make publish
rsync -r -a -v -e ssh --delete --ignore-existing output/ web:/srv/www/rre.nu/
