---
title: How to set up an ajellito instance
name: Getting Started
layout: default
category: navigation
---
## Introduction

This document is about how to setup up Ajellito in a Python virtual
environment.

## Details

Make sure that you have installed the following packages in your
system:
-   python2.5
-   python-dateutil
-   pyExcelerator (optional,
    [http://sourceforge.net/projects/pyexcelerator](http://sourceforge.net/projects/pyexcelerator))
-   matplotlib (optional,
    [http://matplotlib.sourceforge.net/](http://matplotlib.sourceforge.net/))

Install Django. If you already have Django installed, just jump
into the next step, otherwise you'll need to install Django. Take
into account that Ajellito needs Django version 1.0 to run. There
are several ways to install Django. You can follow the Quick
Install Guide from the Django site. I choose to easy install it:

        $ easy_install Django

Clone the Ajellito repo and run the installer script:
        $ git clone git://github.com/friflaj/ajellito.git
        $ cd ajellito
        $ ./agilito/install.py

**IMPORTANT: You don't specifically have to name the project
'ajellito'; it can be anything, as long as it's not *agilito*.**

Synchronize the data base and start the Django development server.
From the ajellito directory run:
        $ python manage.py syncdb
        $ python manage.py runserver

## RSS Feeds

Ajellito offers RSS feeds for your product backlog and iteration.
The domain name for the links in the feed will be determined by the
SITE\_ID in your settings.py, so make sure that the site that
points to has its domain name set correctly in the backend
administration

At this point you should be able to point your browser to
[http://127.0.0.1:8000](http://127.0.0.1:8000) and you should be
asked for authentication. There we need to provide the credentials
that we choose when we ran the manage.py syncdb command.

## Database upgrades

If you're upgrading your ajellito version it could be necessary to
add columns to existing tables. Django doesn't provide a
standardized way to do this, but the install script will attempt to
help you, if you have
[django-command-extensions](http://code.google.com/p/django-command-extensions/)
installed, which is highly recommended.

## Caching

Ajellito can make use of the django caching mechanism, and will do
so when you set it up as per usual in django. Make sure you have
your TIMEZONE set correctly in settings.py; the objects will be
retained longer than you want if you don't.

## Restricted vs. unrestricted story sizes

Ajellito supports both methods of sizing by setting the variable
UNRESTRICTED\_SIZE to True of False in your settings. This setting
is instance-wide and affects all your projects. It is currently not
supported to set this to False after having used projects that were
created while it was set to True.



