# http://www.djangosnippets.org/snippets/67/#c52

from django.conf import settings as _settings
from datetime import datetime, timedelta

def settings(request):
    return {'settings': _settings}
    
def is_css_naked(request):
    return {'is_css_naked': is_date_covered(css_naked_date(), datetime.now())}
    
def is_date_covered(date1, date2):
    if date2 < date1 + timedelta(hours=-12):
        return False
    if date2 > date1 + timedelta(hours=+36):
        return False
    return True
    
def css_naked_date(year=None):
    if year is None: 
        year = datetime.today().year
    d = datetime(year, 4, 5)
    wd = d.isoweekday() # 1=Monday, 2=Tuesday, etc.
    d += timedelta(days=(3 - wd if wd <= 3 else 10 - wd)) # Advance to Wednesday
    return d
    