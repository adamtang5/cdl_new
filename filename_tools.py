'''
Name: filename_tools.py

What:
File name sanitization library
'''


import re

def prep_comp_string(s):
  single_quotes = re.sub('.mp4$', '', re.sub('[`“”’"]', "'", s))

  # print(single_quotes)
  return re.sub(' +', ' ', re.sub('[^a-zA-Z0-9.,$\' +]', '', single_quotes))


def make_valid(s):
  return re.sub('[^\w_.\,)( \'-]', '', s).strip()

#print(make_valid(" Windhorst: The Warriors had a 'glorious' summer"))

def prep_ps_url(url):
  return re.sub('&', '\"&\"', url)

# print(prep_ps_url("https://www.saveoffline.com/get/?i=fFRBZINc8Zku3I9fcfTQxbKr1zOCuDXN&u=lYuat1KxAqLXe6fjAVjiK3jkuuN7uoRB"))

def prep_ps_filename(filename):
  return re.sub('\'', '\'\'', filename)

# print("'" + prep_ps_filename("Drones vs. California's wildfires: How they're helping firefighters") + "'")

def shrink_whitespace(s):
  return re.sub(' +', ' ', s)

