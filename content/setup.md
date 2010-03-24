
There are some changes from [the article on Django Advent][1]

- You don’t need to set up the `/etc/service` directory; this is done for you by 
  `aptitude install daemontools-run`. But you DO need to add `universe` to your list of repositories
  (by uncommenting some lines in `/etc/apt/sources.list`.
  
- Ubuntu is part-way through the migration to using Upstart instead of init.
  Upstart config files are now in `/etc/init` and have a `.conf` suffix.
  The configuration file for `svsvan` is added by `aptitude install daemontools-run`.
  
- Create per-site user with 

    adduser -

  [1]: http://djangoadvent.com/1.2/deploying-django-site-using-fastcgi/