'''
Name: smart_downloader.py
Better names:
  Cache manager

What:
Algorithm to track downloaded items
'''


import json
import re
import local_env

file_suffix = '_vid_cache.json'

''' One-time initialization of cache json files

platforms = ['youtube','espn']

for p in platforms:
  init_dict = {'platform': p, 'vid_ids': []}
  file = open(p + file_suffix, 'w')
  file.write(json.dumps(init_dict))
  file.close()

'''

'''
Formatting:
YouTube Vid ID List:
dict = {"platform": "youtube", "vid_ids": [...]}

ESPN Vid ID List:
dict = {"platform": "espn", "vid_ids": [...]}
'''

# ETCG Exception Phrase
exclude_etcg_titles = ["Office Hours Tech Question and Answers"]


# Check to see if vid_id already exists in cache json
def in_cache(platform, vid_id):
  file = open(local_env.sdl_cache_path + platform + file_suffix, 'r')
  dict = json.loads(file.read())
  file.close()

  return vid_id in dict['vid_ids']

# print(in_cache('espn', '22020137'))

def append_vid(platform, vid_id):
  file = open(local_env.sdl_cache_path + platform + file_suffix, 'r')
  dict = json.loads(file.read())
  file.close()

  dict['vid_ids'].append(vid_id)
  file = open(local_env.sdl_cache_path + platform + file_suffix, 'w')
  file.write(json.dumps(dict))
  file.close()

# append_vid('espn', '20865107')

def fix_cache(platform):
  file = open(local_env.sdl_cache_path + platform + file_suffix, 'r')
  dict = json.loads(file.read())
  file.close()

  # new_dict = {'platform': platform, 'vid_ids': []}
  for n, vid_id in enumerate(dict['vid_ids']):
    if re.search('_', vid_id):
      print(vid_id.split('_')[1])
      dict['vid_ids'][n] = vid_id.split('_')[1]

  file = open(local_env.sdl_cache_path + platform + file_suffix, 'w')
  file.write(json.dumps(dict))
  file.close()

# fix_cache('espn')

def dedup_cache(platform):
  file = open(local_env.sdl_cache_path + platform + file_suffix, 'r')
  dict = json.loads(file.read())
  file.close()

  dict['vid_ids'] = list(set(dict['vid_ids']))

  file = open(local_env.sdl_cache_path + platform + file_suffix, 'w')
  file.write(json.dumps(dict))
  file.close()

# dedup_cache("espn")

authors = ['etcg']

'''

for a in authors:
  init_dict = {'author': a, 'vid_titles': []}
  file = open(local_env.sdl_cache_path + a + file_suffix, 'w')
  file.write(json.dumps(init_dict))
  file.close()

'''

'''
ETCG Vid Title List:
dict = {"author": "etcg", "vid_titles": [
  {"title":...,
   "youtube_vid_id":...,
   "geekvid_vid_id":...}]}
'''


# Check to see if vid_title already exists in etcg cache json
def etcg_title_in_cache(vid_title):
  file = open(local_env.sdl_cache_path + authors[0] + file_suffix, 'r')
  # print(authors[0] + file_suffix)
  dict = json.loads(file.read())
  # print(dict)

  file.close()

  ans = False

  if vid_title not in exclude_etcg_titles:
    for vid_titles in dict['vid_titles']:
      # print(vid_titles)
      if vid_titles['title'] == vid_title:
        ans = True
        break

    '''
    if ans:
      print(vid_title + " is already in cache.")
    else:
      print(vid_title + " is currently not in cache.")
    '''

  return ans

# print(etcg_in_cache("Boeing 737 Max Software FAIL"))

def etcg_title_platform_in_cache(vid_title, platform):
  file = open(local_env.sdl_cache_path + authors[0] + file_suffix, 'r')
  # print(local_env.sdl_cache_path + authors[0] + file_suffix)
  dict = json.loads(file.read())
  # print(dict)

  file.close()

  ans = False
  for vid_titles in dict['vid_titles']:
    # print(vid_titles)
    if vid_titles['title'] == vid_title:
      if platform + '_vid_id' in vid_titles:
        ans = True
        break

  if ans:
    print(vid_title + " (" + platform + ") is already in cache.")
  else:
    print(vid_title + " (" + platform + ") is currently not in cache.")

  return ans

# print(etcg_title_platform_in_cache("Boeing 737 Max Software FAIL", "youtube"))
# print(etcg_title_platform_in_cache("Boeing 737 Max Software FAIL", "geekvid"))


def etcg_append_title(vid_title, platform, vid_id):
  file = open(local_env.sdl_cache_path + authors[0] + file_suffix, 'r')
  dict = json.loads(file.read())
  file.close()

  if platform == 'youtube':
    vid_title_dict = {
      "title": vid_title,
      "youtube_vid_id": vid_id
    }
    dict['vid_titles'].append(vid_title_dict)
    print("Appended: ", vid_title_dict)
  elif platform == 'geekvid':
    vid_title_dict = {
      "title": vid_title,
      "geekvid_vid_id": vid_id
    }
    dict['vid_titles'].append(vid_title_dict)
    print("Appended: ", vid_title_dict)


  file = open(local_env.sdl_cache_path + authors[0] + file_suffix, 'w')
  file.write(json.dumps(dict))
  file.close()


def etcg_append_vid_id(vid_title, platform, vid_id):
  file = open(local_env.sdl_cache_path + authors[0] + file_suffix, 'r')
  dict = json.loads(file.read())
  file.close()
  # print(dict)

  for vid_titles in dict['vid_titles']:
    # print(vid_titles)
    if vid_titles['title'] == vid_title:
      # print(vid_titles)
      if platform == 'youtube':
        vid_titles["youtube_vid_id"] = vid_id
        print("Appended: 'youtube_vid_id' ", vid_id)
      elif platform == 'geekvid':
        vid_titles["geekvid_vid_id"] = vid_id
        print("Appended: 'geekvid_vid_id' ", vid_id)
      break

  file = open(local_env.sdl_cache_path + authors[0] + file_suffix, 'w')
  file.write(json.dumps(dict))
  file.close()


# etcg_append_vid_id('20865107')


def sync_etcg_cache(vid_title, platform, vid_id):
  if not etcg_title_in_cache(vid_title):
    etcg_append_title(vid_title, platform, vid_id)
  else:
    if not etcg_title_platform_in_cache(vid_title, platform):
      etcg_append_vid_id(vid_title, platform, vid_id)
