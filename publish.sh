#!/bin/bash
make publish
scp -r output/* web:/srv/www/rre.nu
