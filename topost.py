#!/usr/bin/env python
import glob
import re
import time
import os

for page in glob.glob('_posts/*.markdown'):
    newpage = page[len('_posts/'):]
    if re.match('[0-9]{4}-[0-9]{2}-[0-9]{2}-', newpage):
        newpage = newpage[11:]
    modified = time.strftime("%Y-%m-%d",time.localtime(os.path.getmtime(page)))

    newpage = '_posts/' + modified + '-' + newpage

    if newpage != page:
        os.rename(page, newpage)
