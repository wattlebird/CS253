months = ('January',
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December')

alphabeta = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
rotedbeta = "nopqrstuvwxyzabcdefghijklmNOPQRSTUVWXYZABCDEFGHIJKLM"
rotdict = dict((alphabeta[i], rotedbeta[i]) for i in range(0, 52))
invdict = dict((rotedbeta[i], alphabeta[i]) for i in range(0, 52))
          
def valid_month(month):
    if month:
        month=month.capitalize()
        if month in months:
            return month

def valid_day(day):
    if day and day.isdigit():
	day=int(day)
        if day>0 and day<=31:
            return day

def valid_year(year):
    if year and year.isdigit():
        year = int(year)
        if year>=1900 and year <=2020:
            return year

def escape_html(s):
    s=s.replace('&','&amp;')
    s=s.replace('<','&lt;')
    s=s.replace('>','&gt;')
    s=s.replace(';','&quot;')
    return s;

def rot13(s):
    newstr = ""
    for w in s[:]:
        if w in alphabeta[:]:
            newstr += rotdict[w]
        else:
            newstr += w
    return newstr
