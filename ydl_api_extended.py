'''
Name: ydl_api_extended.py
Better name:
  ydl engine

What:
  Definition of format ids for multiple platforms: YouTube, ESPN video, etc.
  Template for handling YouTube playlists and ESPN Video categories.
'''
import yt_dlp
from yt_dlp import YoutubeDL
import datetime
import json
from functools import reduce


verbage1 = "Published on "
verbage2 = "Streamed live on "
verbage3 = ["Streamed live ", " ago"]
verbage4 = "Premiered "
verbage5 = ["Premiered ", " ago"]
verbage6 = "Premieres "



# Old standards
'''
yt_formats = {
  'criteria': 'format',
  'labels': {
    'low_res': '18 - 640x360 (360p)',
    'hi_res': '22 - 1280x720 (720p)'
    }
  }
'''

yt_formats = {
  'criteria': 'format_id',
  'labels': {
    'low_res': '18',
    'hi_res': '22'}
}


espn_format_ids = ['http-1200', 'full']
twitter_format_ids = ['hls-1280']

'''
Inputs: list of formats, criteria to look for (e.g. height, or format_note), function to optimize with (e.g. min)
Output: list of formats with optimal values (e.g. only include one format per criterion (height) with optimal (file size)

file = open("ydl_sample.json", 'r')
sample_vid = json.loads(file.read())
file.close()
'''


def filter_by_criteria(l, criteria, value_list):
  return list(filter(lambda x: x[criteria] in value_list, l))


def filter_by_valid_value(l, criteria):
  return list(filter(lambda x: x[criteria] is not None, l))


def optimize_by_criteria(l, criteria, func=min):
  v = []
  for i in l:
    v.append(i[criteria])

  optimal_index = reduce(func, v)

  ans = []
  for i in l:
    if i[criteria] == optimal_index:
      ans.append(i)
  return ans

# print(optimize_by_criteria(sample_vid['formats'], 'filesize'))


'''
mp4_vids = filter_by_criteria(sample_vid['formats'], 'ext', ['mp4'])

for n in yt_formats['labels'].values():
  mp4_vids_of_format = filter_by_criteria(mp4_vids, yt_formats['criteria'], [n])
  print(optimize_by_criteria(mp4_vids_of_format, 'filesize'))
'''


def ydl_get_dict(vid_id):
  ydl = YoutubeDL({'outtmpl': '%(id)s%(ext)s', 'quiet': True})

  with ydl:
    try:
      result = ydl.extract_info(
        'http://www.youtube.com/watch?v=' + vid_id,
        download=False  # We just want to extract the info
      )
    except yt_dlp.utils.DownloadError:
      print("DownloadError: " + vid_id)
      return ydl_get_dict(vid_id)
    except yt_dlp.utils.ExtractorError:
      print("ExtractorError: " + vid_id)


  if 'entries' in result:
    # Can be a playlist or a list of videos
    video = result['entries'][0]
  else:
    # Just a video
    video = result

  # print(video)

  vid_d = {}

  vid_d['vid_id'] = video['id']
  vid_d['title'] = video['title']
  vid_d['upload_date'] = video['upload_date']

  pub_date = datetime.datetime.strptime(video['upload_date'], '%Y%m%d')
  pub_day = pub_date.day
  pub_month = pub_date.month
  pub_year = pub_date.year

  vid_d['pub_date'] = datetime.date(pub_year, pub_month, pub_day)

  vid_d['duration'] = video['duration']
  # vid_d['is_live'] = video['is_live']
  # vid_d['start_time'] = video['start_time']
  # vid_d['end_time'] = video['end_time']

  '''  Typical formats
  '''
  vid_d['formats'] = []
  for vid_format in video['formats']:
    if (vid_format['ext'] == 'mp4') and (vid_format[yt_formats['criteria']] in yt_formats['labels'].values()):
      vid_d['formats'].append(vid_format)

  # YouTube Movies formats
  '''
  vid_d['formats'] = []
  preferred_heights = [360, 720, 1080]
  mp4_vids = filter_by_criteria(filter_by_valid_value(filter_by_criteria(video['formats'], 'ext', ['mp4']), 'filesize'), 'height', preferred_heights)
  # print(mp4_vids)

  vid_d['formats'].append(mp4_vids)

  for n in yt_formats['labels'].values():
    # print(n)
    mp4_vids_of_format = filter_by_criteria(mp4_vids, yt_formats['criteria'], [n])
    # print(mp4_vids_of_format)
    vid_d['formats'].append(optimize_by_criteria(mp4_vids_of_format, 'filesize')[0])
  '''


  return vid_d


# print(ydl_get_dict('qGGGLYVxp4Q'))
# print(ydl_get_dict('iFdLEkVhDRI'))
# print(ydl_get_dict('fIPFyZGEWfU'))

# print(ydl_get_dict('l9vn5UvsHvM'))


def ydl_get_dict_espn(vid_id):
  ydl = YoutubeDL({'outtmpl': '%(id)s%(ext)s', 'quiet': True})
  vid_d = {}

  with ydl:
    try:
      result = ydl.extract_info(
        'http://www.espn.com/video/clip/_/id/' + vid_id,
        download=False  # We just want to extract the info
      )

      if 'entries' in result:
        # Can be a playlist or a list of videos
        video = result['entries'][0]
      else:
        # Just a video
        video = result
      print(video)

      vid_d = {
        'vid_id': video['id'],
        'title': video['title'],
        'duration': video['duration'],
        'description': video['description'],
        'formats': [],
      }

      for vid_format in video['formats']:
        if (vid_format['ext'] == 'mp4') and (vid_format['format_id'] in espn_format_ids):
          vid_d['formats'].append(vid_format)

      # print(vid_d)

    except yt_dlp.utils.DownloadError:

      vid_d['vid_id'] = vid_id

  return vid_d


# print(ydl_get_dict_espn('29990654'))

def ydl_get_dict_mlb(vid_url):
  ydl = YoutubeDL({'outtmpl': '%(id)s%(ext)s', 'quiet': True})

  with ydl:
    result = ydl.extract_info(
      vid_url,
      download=False  # We just want to extract the info
    )

  if 'entries' in result:
    # Can be a playlist or a list of videos
    video = result['entries'][0]
  else:
    # Just a video
    video = result

  print(video)

# ydl_get_dict_mlb("https://www.mlb.com/video/business-of-baseball-mets")


def ydl_get_dict_twitter(vid_url):
  ydl = YoutubeDL({'outtmpl': '%(id)s%(ext)s', 'quiet': True})

  with ydl:
    result = ydl.extract_info(
      vid_url,
      download=False  # We just want to extract the info
    )

  if 'entries' in result:
    # Can be a playlist or a list of videos
    video = result['entries'][0]
  else:
    # Just a video
    video = result

  print(video)

  vid_d = {}

  vid_d['vid_id'] = video['id']
  vid_d['title'] = video['title']
  # vid_d['upload_date'] = video['upload_date']

  '''
  pub_date = datetime.datetime.strptime(video['upload_date'], '%Y%m%d')
  pub_day = pub_date.day
  pub_month = pub_date.month
  pub_year = pub_date.year

  vid_d['pub_date'] = datetime.date(pub_year, pub_month, pub_day)
  
  vid_d['duration'] = video['duration']
  vid_d['is_live'] = video['is_live']
  vid_d['start_time'] = video['start_time']
  vid_d['end_time'] = video['end_time']
  '''

  vid_d['formats'] = []
  for vid_format in video['formats']:
    if (vid_format['ext'] == 'mp4') and (vid_format['format_id'] in twitter_format_ids):
      vid_d['formats'].append(vid_format)

  return vid_d


# print(ydl_get_dict_twitter("https://twitter.com/TastyJapan/status/1156506835081281539"))
# print(ydl_get_dict_twitter("https://twitter.com/i/status/1160385348117024768"))

# ydl = YoutubeDL()
# info = ydl.extract_info('https://www.youtube.com/playlist?list=UUvJJ_dzjViJCoLf5uKUTwoA', download=False)
# print(info)