#!/bin/bash
make publish
rsync -rave ssh output/ web:/srv/www/rre.nu/
