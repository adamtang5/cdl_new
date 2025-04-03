'''
Name: ydl_alg.py

What:
YouTube_dl based playlist downloader alg collection
'''


import requests
from bs4 import BeautifulSoup
import vchannel_data_api
import udl_alg
import ydl_api_extended
import filename_tools
import datetime
import smart_downloader
import datetime_tools
import re
import json
import local_env
import os


exclude_yt_vid_ids = []
exclude_espn_vid_ids = []


'''
Ingestion: Gathering list of IDs from specification (e.g. playlist/single video)

Date: February 12, 2021
'''


def playlist_to_contents_dict(playlist_url, count=40):
  req_prefix = "https://api.feedly.com/v3/streams/contents?streamId=feed/"
  req_suffix = f"&count={str(count)}&ranked=newest&similar=true&findUrlDuplicates=true&ck=1742802754783&ct=feedly.desktop&cv=31.0.2623"
  res = requests.get(req_prefix + playlist_url + req_suffix)
  try:
    data = res.json()
  except ValueError:
    print("Response is not in JSON format")
    data = None

  vids = []
  if data:
    for item in data['items']:
      vids.append({
        'title': item['title'],
        'url': item["alternate"][0]["href"],
      })
  return vids

# print(playlist_to_contents_dict('https://www.youtube.com/playlist?list=UUvJJ_dzjViJCoLf5uKUTwoA'))


def vid_to_contents_dict(vid_url):
  playlist_whole_soup = BeautifulSoup(requests.get(vid_url).text, "html.parser")

  soup_scripts = playlist_whole_soup.find_all("script")
  # print(soup_scripts)
  script_d = []
  for s in soup_scripts:
    # print(s.__dict__["contents"][0])
    if s.__dict__["contents"] != []:
      if re.search('ytInitialData = ', s.__dict__["contents"][0]):
        script_d = json.loads(s.__dict__["contents"][0].split("ytInitialData = ")[1][:-1])

  try:
    contents_d = script_d["contents"]["twoColumnWatchNextResults"]["results"]["results"]["contents"][0]["videoPrimaryInfoRenderer"]
  except KeyError:
    contents_d = script_d["contents"]["twoColumnWatchNextResults"]["results"]["results"]["contents"][1]["videoPrimaryInfoRenderer"]

  return contents_d

# print(vid_to_contents_dict("https://www.youtube.com/watch?v=bosSNSvihpY"))


'''
End of Ingestion Section
'''


'''
Filtering: Weeding out the list by criteria such as date, length, title, cache file, exclusion lists, etc.
'''


def ydl_filter_by_date(vids_d, since_date):
  vids = []



def ydl_playlist_spider(playlist_url, since_date, filter_phrases=[], short_form=True):
  vids_d = playlist_to_contents_dict(playlist_url)
  # print(vids_d)

  vids = []
  title = ''

  # List of videos rendered in playlist
  for vid in vids_d:
    vid_id = vid['url'].split("?v=")[1]
    title = vid['title']

    if not(vchannel_data_api.title_checker(filter_phrases, title)):

      if not (vid_id in exclude_yt_vid_ids) \
        and not (smart_downloader.in_cache('youtube', vid_id)):

          vid_contents_d = vid_to_contents_dict("https://www.youtube.com/watch?v=" + vid_id)
          vid_dateText = vid_contents_d["dateText"]["simpleText"]

          # if 'Premieres' doesn't appear in date_slot_str
          if vid_dateText.find(ydl_api_extended.verbage6) == -1:
            ydl_dict = ydl_api_extended.ydl_get_dict(vid_id)

            if ydl_dict['formats']:
              ydl_dict['title'] = title   # since ydl is unable to extract video titles
              if ydl_dict['pub_date'] >= since_date:
                if not short_form:
                  print(vid_id, ydl_dict['title'])
                  vids.append(ydl_dict)
                else:
                  if ydl_dict['duration'] < 1200:
                    print(vid_id, ydl_dict['title'])
                    vids.append(ydl_dict)
              else:
                break

  return vids

# print(ydl_playlist_spider("https://www.youtube.com/playlist?list=UUvJJ_dzjViJCoLf5uKUTwoA"))


def ydl_playlist_spider_20210212(playlist_url, since_date, filter_phrases=[], short_form=True):
  playlist_whole_soup = BeautifulSoup(requests.get(playlist_url).text, "lxml")
  # print(playlist_whole_soup)
  vids_d = []

  try:
    soup_scripts = playlist_whole_soup.find_all("script")
    # print(soup_scripts)
    meta_script = soup_scripts[32].__dict__["contents"][0]
    # print(meta_script)
  except IndexError:
    print("ydl_playlist_spider IndexError")
    return vids_d
    pass
  else:
    # print(vids_d)

    vids = []

    # List of videos rendered in playlist
    for vid in vids:
      vid_id = vid["playlistVideoRenderer"]["videoId"]
      vid_index = vid["playlistVideoRenderer"]["index"]["simpleText"]
      title = ''

      try:
        title = vid["playlistVideoRenderer"]["title"]["simpleText"]
      except KeyError:
        title = vid["playlistVideoRenderer"]["title"]["runs"][0]["text"]
      # print(vid_id, title)

      if not (smart_downloader.in_cache('youtube', vid_id)):
        print(vid_id, title)
        ydl_dict = ydl_api_extended.ydl_get_dict(vid_id)
        ydl_dict["vid_index"] = vid_index
        vids.append(ydl_dict)

    # print(vids)
    return vids


# print(ydl_playlist_spider_20210212("https://www.youtube.com/playlist?list=UUvJJ_dzjViJCoLf5uKUTwoA", datetime.date(2021, 2, 10)))


def ydl_download_playlist(playlist_name, since_date, format=ydl_api_extended.yt_formats['labels']['low_res'], short_form=True):
  d = vchannel_data_api.lookup_by_source(playlist_name)
  # print(d)

  try:
    vids = ydl_playlist_spider(d['data_source'], since_date, vchannel_data_api.lookup_filter_by_creator(playlist_name), short_form)
    print(playlist_name, vids)
  except TypeError:
    pass
  else:
    for vids_d in vids:
      vid_name = vchannel_data_api.lookup_naming_rules_by_creator(playlist_name)(vids_d['title'])
      request_url = ''
      for vid_format in vids_d['formats']:
        if vid_format[ydl_api_extended.yt_formats['criteria']] == format:
          request_url = vid_format['url']

      print("URL: " + request_url)
      udl_alg.download_video(request_url, vid_name, d['destination_path'])
      smart_downloader.append_vid('youtube', vids_d['vid_id'])


def uploads_tab_to_items_dict(uploads_url):
  uploads_whole_soup = BeautifulSoup(requests.get(uploads_url).text, "html.parser")

  try:
    soup_scripts = uploads_whole_soup.find_all("script")
    # print(soup_scripts[27])
    meta_script = soup_scripts[27].__dict__["contents"][0]
    # print(meta_script)
  except IndexError:
    print("IndexError")
    return []
  else:
    try:
      script_d = json.loads(meta_script.split("ytInitialData = ")[1][:-1])
    except IndexError:
      # print(meta_script)
      print("uploads_tab_to_items_dict IndexError:", uploads_url)
      return uploads_tab_to_items_dict(uploads_url)
    else:
      items_d = script_d["contents"]["twoColumnBrowseResultsRenderer"]["tabs"][1]["tabRenderer"]["content"]["sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"][0]["gridRenderer"]["items"]

  # print(items_d)
  return items_d


def ydl_uploads_tab_spider(uploads_url, since_date, filter_phrases=[], short_form=True):
  vids = []

  items_d = uploads_tab_to_items_dict(uploads_url)

  # List of videos rendered in playlist
  title = ""
  for i in items_d:
    try:
      vid_id = i["gridVideoRenderer"]["videoId"]
      try:
        title = i["gridVideoRenderer"]["title"]["simpleText"]
      except KeyError:
        title = i["gridVideoRenderer"]["title"]["runs"][0]["text"]
    except KeyError:
      pass
    # print("videoID: ", vid_id)

    # print(vid_id, title)
    if not(vchannel_data_api.title_checker(filter_phrases, title)):

      if not (vid_id in exclude_yt_vid_ids) \
        and not (smart_downloader.in_cache('youtube', vid_id)):

          vid_contents_d = vid_to_contents_dict("https://www.youtube.com/watch?v=" + vid_id)
          vid_dateText = vid_contents_d["dateText"]["simpleText"]

          # if 'Premieres' doesn't appear in date_slot_str
          if vid_dateText.find(ydl_api_extended.verbage6) == -1:
            ydl_dict = ydl_api_extended.ydl_get_dict(vid_id)

            if ydl_dict['formats']:
              ydl_dict['title'] = title   # since ydl is unable to extract video titles
              if ydl_dict['pub_date'] >= since_date:
                if not short_form:
                  print(vid_id, ydl_dict['title'])
                  vids.append(ydl_dict)
                else:
                  if ydl_dict['duration'] < 1200:
                    print(vid_id, ydl_dict['title'])
                    vids.append(ydl_dict)
              else:
                  break
  # print(vids)
  return vids

# print(ydl_uploads_tab_spider("https://www.youtube.com/c/ESPN/videos", datetime.date(2020, 7, 23)))


def ydl_download_playlist_old(playlist_name, since_date, format=ydl_api_extended.yt_formats['labels']['low_res'], short_form=True):
  d = vchannel_data_api.lookup_by_source(playlist_name)
  # print(d)

  try:
    vids = ydl_uploads_tab_spider(d['upload_url'], since_date, vchannel_data_api.lookup_filter_by_creator(playlist_name), short_form)
    print(playlist_name, vids)
  except TypeError:
    print("TypeError:", playlist_name)
    pass
  else:
    for vids_d in vids:
      vid_name = vchannel_data_api.lookup_naming_rules_by_creator(playlist_name)(vids_d['title'])
      request_url = ''
      for vid_format in vids_d['formats']:
        if vid_format[ydl_api_extended.yt_formats['criteria']] == format:
          request_url = vid_format['url']

      print("URL: " + request_url)
      udl_alg.download_video(request_url, vid_name, d['destination_path'])
      smart_downloader.append_vid('youtube', vids_d['vid_id'])



def ydl_single_video(vid_url, playlist_name='espn-yt', format=ydl_api_extended.yt_formats['labels']['low_res']):
  # print("Format: " + format)
  d = vchannel_data_api.lookup_by_source(playlist_name)

  vid_d = ydl_api_extended.ydl_get_dict(vid_url.split("?v=")[1].split("&")[0])
  # print(vid_d)
  vid_name = filename_tools.make_valid(vid_d['title'])
  request_url = ''
  for vid_format in vid_d['formats']:
    if vid_format[ydl_api_extended.yt_formats['criteria']] == format:
      request_url = vid_format['url']

  print("URL: " + request_url)
  udl_alg.download_video(request_url, vid_name, d['destination_path'])


'''
ETCG Profile:
* Format: 'medium'
* Filters: NO
* Naming Rules: YES
* Additional Caching: YES
'''


def ydl_etcg_uploads_tab_spider(uploads_url, since_date):
  vids = []

  items_d = uploads_tab_to_items_dict(uploads_url)

  # List of videos rendered in playlist
  for i in items_d:
    try:
      vid_id = i["gridVideoRenderer"]["videoId"]
      # print("videoID: ", vid_id)
      vid_url = "https://www.youtube.com/watch?v=" + vid_id

      if not (vid_id in exclude_yt_vid_ids) \
        and not (smart_downloader.in_cache('youtube', vid_id)):
          vid_contents_d = vid_to_contents_dict(vid_url)
          # print(vid_contents_d)

          # vid_title = vid_contents_d["title"]["runs"][0]["text"]
          vid_dateText = vid_contents_d["dateText"]["simpleText"]
          # print(vid_title, vid_dateText)

          # if 'Premieres' doesn't appear in date_slot_str
          if vid_dateText.find(ydl_api_extended.verbage6) == -1:
            # print(vid_id, title)

            ydl_dict = ydl_api_extended.ydl_get_dict(vid_id)
            # print(ydl_dict)
            title = ydl_dict['title']

            cache_title = filename_tools.make_valid(filename_tools.prep_comp_string(title))
            # print(vid_id, comp_title)

            if ydl_dict['formats'] and (ydl_dict['pub_date'] >= since_date):
              if smart_downloader.etcg_title_in_cache(cache_title):
                smart_downloader.sync_etcg_cache(cache_title, 'youtube', vid_id)
              else:
                print(vid_id, ydl_dict['title'], vid_dateText)
                vids.append(ydl_dict)
                # print("Appended: ", ydl_dict)
            else:
              break
    except KeyError:
      pass

  # print(vids)
  return vids

# print(ydl_etcg_spider(datetime.date(2020, 5, 1)))
# print(ydl_playlist_spider("https://youtube.com/playlist?list=UUvJJ_dzjViJCoLf5uKUTwoA", datetime.date(2019, 4, 14)))
# print(ydl_etcg_spider(vchannel_data_api.lookup_by_source('etcg')['data_source'], datetime.date(2019, 9, 10)))


def ydl_etcg_playlist_spider(playlist_url, since_date):
  # return ydl_playlist_spider(playlist_url, since_date, short_form=False)
  vids_d = playlist_to_contents_dict(playlist_url)
  vids = []
  title = ''

  # List of videos rendered in playlist
  for vid in vids_d:
    vid_id = ''
    try:
      vid_id = vid["playlistVideoRenderer"]["videoId"]
      # vid_index = vid["playlistVideoRenderer"]["index"]["simpleText"]
      vid_url = "https://www.youtube.com/watch?v=" + vid_id

      '''
      try:
        title = vid["playlistVideoRenderer"]["title"]["simpleText"]
      except KeyError:
        title = vid["playlistVideoRenderer"]["title"]["runs"][0]["text"]
      # print(vid_id, title)
      '''

    except KeyError:
      pass

    # print("videoID: ", vid_id)

    if not (vid_id in exclude_yt_vid_ids) \
      and not (smart_downloader.in_cache('youtube', vid_id)):
        vid_contents_d = vid_to_contents_dict(vid_url)
        # print(vid_contents_d)

        # vid_title = vid_contents_d["title"]["runs"][0]["text"]
        vid_dateText = vid_contents_d["dateText"]["simpleText"]
        # print(vid_title, vid_dateText)

        # if 'Premieres' doesn't appear in date_slot_str
        if vid_dateText.find(ydl_api_extended.verbage6) == -1:
          # print(vid_id, title)

          ydl_dict = ydl_api_extended.ydl_get_dict(vid_id)
          # print(ydl_dict)
          title = ydl_dict['title']

          cache_title = filename_tools.make_valid(filename_tools.prep_comp_string(title))
          # print(vid_id, comp_title)

          if ydl_dict['formats'] and (ydl_dict['pub_date'] >= since_date):
            if smart_downloader.etcg_title_in_cache(cache_title):
              smart_downloader.sync_etcg_cache(cache_title, 'youtube', vid_id)
            else:
              print(vid_id, ydl_dict['title'], vid_dateText)
              vids.append(ydl_dict)
              # print("Appended: ", ydl_dict)
          else:
            break

  # print(vids)
  return vids


def ydl_download_etcg(playlist_name, since_date, format=ydl_api_extended.yt_formats['labels']['low_res']):
  d = vchannel_data_api.lookup_by_source(playlist_name)

  try:
    vids = ydl_etcg_playlist_spider(d['data_source'], since_date)
    print(playlist_name, vids)
  except TypeError:
    pass
  else:
    for vids_d in vids:
      vid_name = filename_tools.make_valid(vids_d['title'])
      datestr = vids_d['upload_date']

      request_url = ''
      for vid_format in vids_d['formats']:
        if vid_format[ydl_api_extended.yt_formats['criteria']] == format:
          request_url = vid_format['url']

      print("URL: " + request_url)
      udl_alg.download_video(request_url, datestr + ' - ' + vid_name, d['destination_path'], ext=".mp4")
      smart_downloader.append_vid('youtube', vids_d['vid_id'])

      # ETCG Vid Cache JSON
      cache_title = filename_tools.make_valid(filename_tools.prep_comp_string(vids_d['title']))

      smart_downloader.sync_etcg_cache(cache_title, 'youtube', vids_d['vid_id'])



def ydl_download_etcg_bundle(since_date, format=ydl_api_extended.yt_formats['labels']['low_res']):
  for cid in vchannel_data_api.etcg_ids:
    ydl_download_etcg(cid, since_date, format)



'''
CNBC Profile:
* Format: 'medium'
* Filters: YES
* Naming Rules: NO
'''

def ydl_cnbc_spider(since_date):
  playlist_url = vchannel_data_api.lookup_by_source('cnbc')['data_source']
  playlist_whole_soup = BeautifulSoup(requests.get(playlist_url).text, "lxml")
  vids_table_soup = BeautifulSoup(str(playlist_whole_soup.find_all("tbody")[0]), "lxml")
  #print(vids_table_soup)

  vids = []
  for vids_row_li in vids_table_soup.find_all("tr", ["pl-video", "yt-uix-tile"]):
    title = vids_row_li.get("data-title")
    #print(title)
    if not(vchannel_data_api.title_checker(vchannel_data_api.cnbc_phrases, title)):
      vids_row_soup = BeautifulSoup(str(vids_row_li),"lxml")
      href = vids_row_soup.find("a", "pl-video-title-link").get("href")
      vid_id = href.split("?v=")[1].split("&")[0]


      if not (vid_id in exclude_yt_vid_ids) \
        and not (smart_downloader.in_cache('youtube', vid_id)):
          ydl_dict = ydl_api_extended.ydl_get_dict(vid_id)
          # print(ydl_dict['formats'])

          if ydl_dict['formats']:
            # print(ydl_dict['pub_date'])
            if ydl_dict['pub_date'] >= since_date:
              print(vid_id, ydl_dict['title'])
              vids.append(ydl_dict)
            else:
              break

  return vids

# print(ydl_cnbc_spider(datetime.date(2019, 4, 14)))


def ydl_download_cnbc(since_date, format=ydl_api_extended.yt_formats['labels']['low_res']):
  d = vchannel_data_api.lookup_by_source('cnbc')

  for vids_d in ydl_cnbc_spider(since_date):
    vid_name = filename_tools.make_valid(vids_d['title'])

    request_url = ''
    for vid_format in vids_d['formats']:
      if vid_format[ydl_api_extended.yt_formats['criteria']] == format:
        request_url = vid_format['url']

    # print(request_url)
    udl_alg.download_video(request_url, vid_name, d['destination_path'])
    smart_downloader.append_vid('youtube', vids_d['vid_id'])


'''
CNET Profile:
* Format: 'medium'
* Filters: YES
* Naming Rules: YES
'''

def ydl_cnet_spider(since_date):
  playlist_url = vchannel_data_api.lookup_by_source('cnet')['data_source']
  playlist_whole_soup = BeautifulSoup(requests.get(playlist_url).text, "lxml")
  vids_table_soup = BeautifulSoup(str(playlist_whole_soup.find_all("tbody")[0]), "lxml")
  #print(vids_table_soup)

  vids = []
  for vids_row_li in vids_table_soup.find_all("tr", ["pl-video", "yt-uix-tile"]):
    title = vids_row_li.get("data-title")
    #print(title)
    if not(vchannel_data_api.title_checker(vchannel_data_api.cnet_phrases, title)):
      vids_row_soup = BeautifulSoup(str(vids_row_li),"lxml")
      href = vids_row_soup.find("a", "pl-video-title-link").get("href")
      vid_id = href.split("?v=")[1].split("&")[0]


      if not (vid_id in exclude_yt_vid_ids) \
        and not (smart_downloader.in_cache('youtube', vid_id)):
          ydl_dict = ydl_api_extended.ydl_get_dict(vid_id)
          # print(ydl_dict['formats'])

          if ydl_dict['formats']:
            # print(ydl_dict['pub_date'])
            if ydl_dict['pub_date'] >= since_date \
              and ydl_dict['duration'] < 1200:
                print(vid_id, ydl_dict['title'])
                vids.append(ydl_dict)
            else:
              break

  return vids

# print(ydl_cnet_spider(datetime.date(2019, 4, 14)))


def ydl_download_cnet(since_date, format=ydl_api_extended.yt_formats['labels']['low_res']):
  d = vchannel_data_api.lookup_by_source('cnet')

  for vids_d in ydl_cnet_spider(since_date):
    vid_name = ''

    if vids_d['title'].endswith(" Watch This Space"):
      vid_name = 'WTS ' + filename_tools.make_valid(vids_d['title']).split(' Watch This Space')[0]
    elif vids_d['title'].endswith(" What the Future"):
      vid_name = 'WTF ' + filename_tools.make_valid(vids_d['title']).split(' What the Future')[0]
    else:
      vid_name = filename_tools.make_valid(vids_d['title'])

    request_url = ''
    for vid_format in vids_d['formats']:
      if vid_format[ydl_api_extended.yt_formats['criteria']] == format:
        request_url = vid_format['url']

    # print(request_url)
    udl_alg.download_video(request_url, vid_name, d['destination_path'])
    smart_downloader.append_vid('youtube', vids_d['vid_id'])


'''
MKBHD Profile:
* Format: 'medium'
* Filters: NO
* Naming Rules: NO
'''

'''
The Verge Profile:
* Format: 'medium'
* Filters: NO
* Naming Rules: NO
'''

'''
ESPN Profile:
* Format: 'medium'
* Filters: YES
* Naming Rules: NO
'''

def ydl_espn_yt_spider(since_date):
  playlist_url = vchannel_data_api.lookup_by_source('espn-yt')['data_source']
  playlist_whole_soup = BeautifulSoup(requests.get(playlist_url).text, "lxml")
  vids_table_soup = BeautifulSoup(str(playlist_whole_soup.find_all("tbody")[0]), "lxml")
  #print(vids_table_soup)

  vids = []
  for vids_row_li in vids_table_soup.find_all("tr", ["pl-video", "yt-uix-tile"]):
    title = vids_row_li.get("data-title")
    #print(title)
    if not(vchannel_data_api.title_checker(vchannel_data_api.espn_phrases, title)):
      vids_row_soup = BeautifulSoup(str(vids_row_li),"lxml")
      href = vids_row_soup.find("a", "pl-video-title-link").get("href")
      vid_id = href.split("?v=")[1].split("&")[0]


      if not (vid_id in exclude_yt_vid_ids) \
        and not (smart_downloader.in_cache('youtube', vid_id)):
          ydl_dict = ydl_api_extended.ydl_get_dict(vid_id)
          # print(ydl_dict['formats'])

          if ydl_dict['formats']:
            # print(ydl_dict['pub_date'])
            if ydl_dict['pub_date'] >= since_date:
              print(vid_id, ydl_dict['title'])
              vids.append(ydl_dict)
            else:
              break

  return vids

# print(ydl_espn_spider(datetime.date(2019, 4, 14)))


def ydl_download_espn_yt(since_date, format=ydl_api_extended.yt_formats['labels']['low_res']):
  d = vchannel_data_api.lookup_by_source('espn-yt')

  for vids_d in ydl_espn_yt_spider(since_date):
    vid_name = filename_tools.make_valid(vids_d['title'])

    request_url = ''
    for vid_format in vids_d['formats']:
      if vid_format[ydl_api_extended.yt_formats['criteria']] == format:
        request_url = vid_format['url']

    # print(request_url)
    udl_alg.download_video(request_url, vid_name, d['destination_path'])
    smart_downloader.append_vid('youtube', vids_d['vid_id'])


def ydl_espn_group_spider(url):
  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
  source_code = requests.get(url, headers=headers)
  plain_text = source_code.text
  # print(plain_text)

  whole_soup = BeautifulSoup(plain_text, "lxml")
  vids_soup = BeautifulSoup(str(whole_soup.find_all("div", "vid-page-bottom")[0]), "lxml")
  # print(vids_soup)


  vids = []
  for vid_li in vids_soup.find_all("li"):
    vid_li_soup = BeautifulSoup(str(vid_li), "lxml")
    vid_title = vid_li_soup.find("h4").string
    vid_length = vid_li_soup.find("div", "time-stamp").string
    dl_url = vid_li_soup.find("a").get("href")
    vid_id = vid_li_soup.find("a").get("id").split('_')[1]


    if not (vid_id in exclude_espn_vid_ids) \
      and not (smart_downloader.in_cache('espn', vid_id)) \
      and datetime_tools.at_least_timedelta(datetime_tools.string_to_timedelta(vid_length), seconds=30) \
      and not(vchannel_data_api.title_checker(vchannel_data_api.espn_phrases, vid_title)):
        print(vid_id, vid_title, vid_length, dl_url)
        vids.append(ydl_api_extended.ydl_get_dict_espn(vid_id))

  return vids


def ydl_espn_archive_spider(url):
  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
  source_code = requests.get(url, headers=headers)
  plain_text = source_code.text
  # print(plain_text)

  whole_soup = BeautifulSoup(plain_text, "lxml")
  vids_soup = BeautifulSoup(str(whole_soup.find_all("ul")), "lxml")
  # print(len(vids_soup.find_all("ul")))

  vids = []
  for vid_ul in BeautifulSoup(str(vids_soup.find_all("ul")[0]), "lxml"):
    for vid_li in vid_ul.find_all("li"):
      vid_li_soup = BeautifulSoup(str(vid_li), "lxml")
      vid_title = vid_li_soup.find("a").string
      vid_url = vid_li_soup.find("a").get("href")
      vid_id = vid_url.split('=')[1]

      if vid_id not in exclude_espn_vid_ids \
        and not smart_downloader.in_cache('espn', vid_id) \
        and not vchannel_data_api.title_checker(vchannel_data_api.espn_phrases, vid_title):
          vid_d = ydl_api_extended.ydl_get_dict_espn(vid_id)
          if 'duration' in vid_d and vid_d['duration'] >= 30:
            vids.append(vid_d)

  return vids

# ydl_espn_archive_spider("http://www.espn.com/video/archive")


def ydl_download_espn_group(group_name):
  # print(group_name)
  d = vchannel_data_api.lookup_by_source(group_name)
  # print(d)

  for vids_d in ydl_espn_group_spider(d['data_source']):
    try:
      vid_name = filename_tools.make_valid(vids_d['title'])
    except KeyError:
      smart_downloader.append_vid('espn', vids_d['vid_id'])
    else:
      request_url = ''
      for vid_format in vids_d['formats']:
        if vid_format['format_id'] in ydl_api_extended.espn_format_ids:
          request_url = vid_format['url']

          print(re.search("_SOT", request_url, re.IGNORECASE), "URL: " + request_url)
          if re.search("_SOTFULL", request_url, re.IGNORECASE) == None:
            # print("URL: " + request_url)
            udl_alg.download_video(request_url, vid_name, d['destination_path'])
            smart_downloader.append_vid('espn', vids_d['vid_id'])
          else:
            smart_downloader.append_vid('espn', vids_d['vid_id'])


  if 'alt_data_source' in d:
    for vids_d in ydl_espn_archive_spider(d['alt_data_source']):
      try:
        vid_name = filename_tools.make_valid(vids_d['title'])
      except KeyError:
        smart_downloader.append_vid('espn', vids_d['vid_id'])
      else:
        request_url = ''
        for vid_format in vids_d['formats']:
          if vid_format['format_id'] in ydl_api_extended.espn_format_ids:
            request_url = vid_format['url']

            print(re.search("_SOT", request_url, re.IGNORECASE), "URL: " + request_url)
            if re.search("_SOTFULL", request_url, re.IGNORECASE) == None:
              # print("URL: " + request_url)
              udl_alg.download_video(request_url, vid_name, d['destination_path'])
              smart_downloader.append_vid('espn', vids_d['vid_id'])
            else:
              smart_downloader.append_vid('espn', vids_d['vid_id'])


'''
MLB Profile:
* Format: 'medium'
* Filters: NO
* Naming Rules: YES
'''

def ydl_mlb_group_spider(url, since_date):
  site_prefix = 'https://www.mlb.com'

  headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
  source_code = requests.get(url, headers=headers)
  plain_text = source_code.text
  # print(plain_text)

  whole_soup = BeautifulSoup(plain_text, "lxml")
  # print(whole_soup)

  vids = []
  for card in whole_soup.select('a[class*="ContentCard__Card-sc-"]'):
    vid_page_url = site_prefix + card.get("href")
    vid_length = card.select('p[class*="ContentCard__Duration-sc"]')[0].string
    vid_title = card.select('h3[class*="ContentCard__Title-sc"]')[0].string
    vid_date = datetime.datetime.strptime(card.select('p[class*="ContentCard__Date-sc"]')[0].string, "%B %d, %Y").date()
    # print(vid_url, vid_title, vid_date, vid_length)

    if vid_date >= since_date:
      if ydl_api_extended.ydl_get_dict_mlb(vid_page_url):
        vids.append({
          'url': ydl_api_extended.ydl_get_dict_mlb(vid_page_url),
          'title': vid_title,
          'date': vid_date,
          'length': vid_length,
        })

  return vids

print(ydl_mlb_group_spider('https://www.mlb.com/video/topic/daily-recaps', datetime.date(2025, 4, 1)))


def ydl_download_mlb_group(group_url, since_date):
  for vids_d in ydl_espn_group_spider(group_url):
    try:
      vid_name = filename_tools.make_valid(vids_d['title'])
    except KeyError:
      print("KeyError")
    else:
      pass


# udl_alg.download_video(
#   'https://mlb-cuts-diamond.mlb.com/FORGE/2025/2025-03/31/f5088e44-b754f098-6b50a13e-csvm-diamondgcp-asset.m3u8',
#   '20250331-WSH-TOR.mp4',
#   local_env.espn_video_path)

'''
CUAU Profile:
* Format: 'medium'
* Filters: NO
* Naming Rules: YES
'''

def ydl_cuau_spider(playlist_url, since_date):
  vids = []

  # playlist_url = vchannel_data_api.lookup_by_source(cid)['data_source']
  playlist_whole_soup = BeautifulSoup(requests.get(playlist_url).text, "lxml")
  try:
    vids_table_soup = BeautifulSoup(str(playlist_whole_soup.find_all("tbody")[0]), "lxml")
  except IndexError:
    return vids
    pass
  else:
    # print(vids_table_soup)

    for vids_row_li in vids_table_soup.find_all("tr", ["pl-video", "yt-uix-tile"]):
      # title = vids_row_li.get("data-title")
      #print(title)

      vids_row_soup = BeautifulSoup(str(vids_row_li),"lxml")
      href = vids_row_soup.find("a", "pl-video-title-link").get("href")
      vid_id = href.split("?v=")[1].split("&")[0]

      if not (vid_id in exclude_yt_vid_ids) \
        and not (smart_downloader.in_cache('youtube', vid_id)):
          ydl_dict = ydl_api_extended.ydl_get_dict(vid_id)
          # print(ydl_dict['formats'])

          if ydl_dict['formats']:
            # print(ydl_dict['pub_date'])
            if ydl_dict['pub_date'] >= since_date:
              ydl_dict['title'] = "CU " + ydl_dict['title'].split(' China Uncensored')[0]
              print(vid_id, ydl_dict['title'])
              vids.append(ydl_dict)
            else:
              break

  return vids

# print(ydl_cuau_spider(datetime.date(2019, 9, 10)))


def ydl_download_cuau(playlist_name, since_date, format=ydl_api_extended.yt_formats['labels']['low_res']):
  d = vchannel_data_api.lookup_by_source(playlist_name)

  # print(len(cuau_spider(since_date)))
  for vids_d in ydl_cuau_spider(d['data_source'], since_date):
    vid_name = ''
    if vids_d['title'].endswith(" China Uncensored"):
      vid_name = 'CU ' + filename_tools.make_valid(vids_d['title']).split(' China Uncensored')[0]
    elif vids_d['title'].endswith(" America Uncovered"):
      vid_name = 'AU ' + filename_tools.make_valid(vids_d['title']).split(' America Uncovered')[0]
    else:
      vid_name = filename_tools.make_valid(vids_d['title'])


    request_url = ''
    for vid_format in vids_d['formats']:
      if vid_format[ydl_api_extended.yt_formats['criteria']] == format:
        request_url = vid_format['url']

    print("URL: " + request_url)
    udl_alg.download_video(request_url, vid_name, d['destination_path'])
    smart_downloader.append_vid('youtube', vids_d['vid_id'])


def ydl_download_cuau_bundle(since_date):
  for cid in vchannel_data_api.cuau_ids:
    ydl_download_cuau(cid, since_date)




'''
Bible Project Profile:
* Format: ydl_api_extended.yt_formats['labels']['hi_res']
* Sub-Playlists: YES
* Filters: NO
* Naming Rules: YES
'''

def ydl_bible_project_spider():
  vids = []
  for playlists in vchannel_data_api.lookup_playlists_by_source('bible-project')['playlists']:
    playlist_url = playlists['data_source']
    playlist_whole_soup = BeautifulSoup(requests.get(playlist_url).text, "lxml")
    try:
      vids_table_soup = BeautifulSoup(str(playlist_whole_soup.find_all("tbody")[0]), "lxml")
    except IndexError:
      pass
    else:
      #print(vids_table_soup)

      for vids_row_li in vids_table_soup.find_all("tr", ["pl-video", "yt-uix-tile"]):
        title = vids_row_li.get("data-title")
        #print(title)

        vids_row_soup = BeautifulSoup(str(vids_row_li), "lxml")
        href = vids_row_soup.find("a", "pl-video-title-link").get("href")
        vid_id = href.split("?v=")[1].split("&")[0]


        if not (vid_id in exclude_yt_vid_ids) \
          and not (smart_downloader.in_cache('youtube', vid_id)):
            ydl_dict = ydl_api_extended.ydl_get_dict(vid_id)
            # print(ydl_dict['formats'])

            if ydl_dict['formats']:
              print(vid_id, ydl_dict['title'])

              '''
              if ydl_dict['pub_date'] < datetime.date.today():
                smart_downloader.append_vid('youtube', vid_id)
              else:
                vids.append(ydl_dict)
              '''
              vids.append(ydl_dict)

  return vids

# print(bible_project_spider())

def ydl_download_bible_project():
  d = vchannel_data_api.lookup_playlists_by_source('bible-project')

  for vids_d in ydl_bible_project_spider():
    vid_name = filename_tools.make_valid(vids_d['title'])

    request_url = ''
    for vid_format in vids_d['formats']:
      if vid_format[ydl_api_extended.yt_formats['criteria']] == ydl_api_extended.yt_formats['labels']['hi_res']:
        request_url = vid_format['url']

    # print(request_url)
    udl_alg.download_video(request_url, vid_name, d['destination_path'])
    smart_downloader.append_vid('youtube', vids_d['vid_id'])


def ydl_bible_project_canto_spider():
  vids = []
  for playlists in vchannel_data_api.lookup_playlists_by_source('bible-project-canto')['playlists']:
    playlist_url = playlists['data_source']
    playlist_whole_soup = BeautifulSoup(requests.get(playlist_url).text, "lxml")
    try:
      vids_table_soup = BeautifulSoup(str(playlist_whole_soup.find_all("tbody")[0]), "lxml")
    except IndexError:
      pass
    else:
      #print(vids_table_soup)

      for vids_row_li in vids_table_soup.find_all("tr", ["pl-video", "yt-uix-tile"]):
        title = vids_row_li.get("data-title")
        #print(title)

        vids_row_soup = BeautifulSoup(str(vids_row_li), "lxml")
        href = vids_row_soup.find("a", "pl-video-title-link").get("href")
        vid_id = href.split("?v=")[1].split("&")[0]


        if not (vid_id in exclude_yt_vid_ids) \
          and not (smart_downloader.in_cache('youtube', vid_id)):
            ydl_dict = ydl_api_extended.ydl_get_dict(vid_id)
            # print(ydl_dict['formats'])

            if ydl_dict['formats']:
              print(vid_id, ydl_dict['title'])

              vids.append(ydl_dict)

  return vids

# print(bible_project_spider())

def ydl_download_bible_project_canto():
  d = vchannel_data_api.lookup_playlists_by_source('bible-project-canto')

  for vids_d in ydl_bible_project_canto_spider():
    vid_name = filename_tools.make_valid(vids_d['title'])

    request_url = ''
    for vid_format in vids_d['formats']:
      if vid_format[ydl_api_extended.yt_formats['criteria']] == ydl_api_extended.yt_formats['labels']['hi_res']:
        request_url = vid_format['url']

    # print(request_url)
    udl_alg.download_video(request_url, vid_name, d['destination_path'])
    smart_downloader.append_vid('youtube', vids_d['vid_id'])


def ydl_bible_project_mandarin_spider():
  vids = []
  for playlists in vchannel_data_api.lookup_playlists_by_source('bible-project-mandarin')['playlists']:
    playlist_url = playlists['data_source']
    playlist_whole_soup = BeautifulSoup(requests.get(playlist_url).text, "lxml")
    try:
      vids_table_soup = BeautifulSoup(str(playlist_whole_soup.find_all("tbody")[0]), "lxml")
    except IndexError:
      pass
    else:
      #print(vids_table_soup)

      for vids_row_li in vids_table_soup.find_all("tr", ["pl-video", "yt-uix-tile"]):
        title = vids_row_li.get("data-title")
        #print(title)

        vids_row_soup = BeautifulSoup(str(vids_row_li), "lxml")
        href = vids_row_soup.find("a", "pl-video-title-link").get("href")
        vid_id = href.split("?v=")[1].split("&")[0]


        if not (vid_id in exclude_yt_vid_ids) \
          and not (smart_downloader.in_cache('youtube', vid_id)):
            ydl_dict = ydl_api_extended.ydl_get_dict(vid_id)
            # print(ydl_dict['formats'])

            if ydl_dict['formats']:
              print(vid_id, ydl_dict['title'])

              vids.append(ydl_dict)

  return vids

# print(bible_project_spider())

def ydl_download_bible_project_mandarin():
  d = vchannel_data_api.lookup_playlists_by_source('bible-project-mandarin')

  for vids_d in ydl_bible_project_mandarin_spider():
    vid_name = filename_tools.make_valid(vids_d['title'])

    request_url = ''
    for vid_format in vids_d['formats']:
      if vid_format[ydl_api_extended.yt_formats['criteria']] == ydl_api_extended.yt_formats['labels']['hi_res']:
        request_url = vid_format['url']

    # print(request_url)
    udl_alg.download_video(request_url, vid_name, d['destination_path'])
    smart_downloader.append_vid('youtube', vids_d['vid_id'])


'''
ThreatWire Profile:
* Format: 'medium'
* Filters: NO
* Naming Rules: YES
'''

def ydl_download_tw(since_date, format=ydl_api_extended.yt_formats['labels']['low_res']):
  d = vchannel_data_api.lookup_by_source('threat-wire')

  for vids_d in ydl_playlist_spider(d['data_source'], datetime_tools.day_before(datetime_tools.day_before(datetime_tools.day_before(since_date)))):
    vid_name = 'TW ' + filename_tools.make_valid(vids_d['title']).split(' - ThreatWire')[0]

    request_url = ''
    for vid_format in vids_d['formats']:
      if vid_format[ydl_api_extended.yt_formats['criteria']] == format:
        request_url = vid_format['url']

    # print(request_url)
    udl_alg.download_video(request_url, vid_name, d['destination_path'])
    smart_downloader.append_vid('youtube', vids_d['vid_id'])


'''
Computerphile/Numberphile/Numberphile2 Profile:
* Format: 'medium'
* Filters: NO
* Naming Rules: NO
'''


'''
HT Profile:
* Format: 'medium'
* Filters: NO
* Naming Rules: YES
'''


'''
KhanAcademy Profile:
* Format: ydl_api_extended.yt_formats['labels']['hi_res']
* Filters: YES
* Naming Rules: NO
'''


'''
Tom Scott Profile:
* Format: 'medium'
* Filters: YES
* Naming Rules: YES
'''


'''
NFL Highlights Profile:
* Format: ydl_api_extended.yt_formats['labels']['hi_res']
* Filters: YES
* Naming Rules: YES
'''

#Download NFL Full Game Highlights form YouTube
def ydl_nfl_youtube_spider(week, season):
  vids = []
  playlists_d = channel_vids_tab_to_playlists_dict('nfl-official')
  # print(playlists_d)

  match_str = ''
  if week in range(1, 18):
    match_str = "Game Highlights (Week " + str(week) + ") | NFL " + str(season)
  elif week == 18:
    match_str = "Game Highlights (Super Wild Card Weekend) | NFL " + str(season)
  elif week == 19:
    match_str = "Game Highlights (Divisional Round) | NFL " + str(season)
  elif week == 20:
    match_str = "Game Highlights (Conference Championships) | NFL " + str(season)
  elif week == 21:
    match_str = "Super Bowl LV Highlights"

  game_highlights_playlist_id = ''

  for pl in playlists_d:
    if pl["gridPlaylistRenderer"]["title"]["runs"][0]["text"] == match_str:
      game_highlights_playlist_id = pl["gridPlaylistRenderer"]["title"]["runs"][0]["navigationEndpoint"]["watchEndpoint"]["playlistId"]

  if game_highlights_playlist_id != '':
    vids_d = playlist_to_contents_dict("https://www.youtube.com/playlist?list=" + game_highlights_playlist_id)
    print(season, "Week", week, "Playlist ID:", game_highlights_playlist_id)

    key_phrase = ''
    if week in range(1, 18):
      key_phrase = ' Week ' + str(week) + ' Highlights | NFL ' + str(season)
    elif week == 18:
      key_phrase = ' Super Wild Card Weekend Highlights | NFL ' + str(season) + ' Playoffs'
    elif week == 19:
      key_phrase = ' Divisional Round Highlights | NFL ' + str(season) + ' Playoffs'
    elif week == 20:
      key_phrase = 'FC Championship Highlights | NFL ' + str(season) + ' Playoffs'
    elif week == 21:
      key_phrase = ' | Super Bowl LV Game Highlights'
    #print(key_phrase)

    # print(vids_d)
    # List of videos rendered in playlist
    for vid in vids_d:
      vid_id = vid["playlistVideoRenderer"]["videoId"]
      title = ''

      try:
        title = vid["playlistVideoRenderer"]["title"]["simpleText"]
      except KeyError:
        title = vid["playlistVideoRenderer"]["title"]["runs"][0]["text"]
      # print(vid_id, title)

      if title.endswith(key_phrase):
        matchup_str = title.split(key_phrase)[0]

        if not (smart_downloader.in_cache('youtube', vid_id)):
          print(vid_id, title, matchup_str)
          ydl_dict = ydl_api_extended.ydl_get_dict(vid_id)
          ydl_dict['matchup'] = matchup_str
          vids.append(ydl_dict)

  # print(vids)
  return vids

# print(ydl_nfl_youtube_spider(2, 2020))


def ydl_download_nfl_highlights(week, season):
  d = vchannel_data_api.lookup_by_source('nfl-official')

  for vids_d in ydl_nfl_youtube_spider(week, season):
    vid_name = ''
    if week in range(1, 18):
      vid_name = filename_tools.make_valid("Wk " + str(week) + ' ' + vids_d['matchup'])
    elif week == 18:
      vid_name = filename_tools.make_valid("WC " + vids_d['matchup'])
    elif week == 19:
      vid_name = filename_tools.make_valid("Div " + vids_d['matchup'])
    elif week == 20:
      vid_name = filename_tools.make_valid(vids_d['matchup'][-1] + "FC Champ "+ vids_d['matchup'][0:-2])
    elif week == 21:
      vid_name = filename_tools.make_valid("SB " + vids_d['matchup'])

    request_url = ''
    for vid_format in vids_d['formats']:
      if vid_format[ydl_api_extended.yt_formats['criteria']] == ydl_api_extended.yt_formats['labels']['hi_res']:
        request_url = vid_format['url']

    folder_name = ''
    if week in range(1, 18):
      folder_name = 'Wk ' + str(week) + '\\'
    elif week == 18:
      folder_name = 'Wk ' + str(week) + ' WC\\'
    elif week == 19:
      folder_name = 'Wk ' + str(week) + ' Div\\'
    elif week == 20:
      folder_name = 'Wk ' + str(week) + ' Conf Champ\\'
    elif week == 21:
      folder_name = 'Wk ' + str(week) + ' SB\\'

    udl_alg.download_video(request_url, vid_name, d['destination_path'] + folder_name)
    smart_downloader.append_vid('youtube', vids_d['vid_id'])



#download_nfl_highlights(5)


'''
Download all videos from a single playlist:
* Format: ydl_api_extended.yt_formats['labels']['hi_res']
* Filters: NO
* Naming Rules: YES
'''


def ydl_download_single_playlist(playlist_url, playlist_name):
  parent_dir = local_env.video_root + local_env.tech_training_path
  path = os.path.join(parent_dir, playlist_name)

  try:
    os.mkdir(path)
  except FileExistsError:
    pass

  for vid_d in ydl_playlist_spider(playlist_url):
    vid_name = vid_d["vid_index"] + " - " + filename_tools.make_valid(vid_d["title"])
    request_url = ''
    for vid_format in vid_d['formats']:
      if vid_format[ydl_api_extended.yt_formats['criteria']] == ydl_api_extended.yt_formats['labels']['hi_res']:
        request_url = vid_format['url']

    udl_alg.download_video(request_url, vid_name, path + "\\")
    smart_downloader.append_vid('youtube', vid_d['vid_id'])


def ydl_playlist_spider_obsolete(playlist_url, since_date, filter_phrases=[], short_form=True):
  playlist_whole_soup = BeautifulSoup(requests.get(playlist_url).text, "lxml")
  # print(playlist_whole_soup)
  vids = []

  try:
    vids_table_soup = BeautifulSoup(str(playlist_whole_soup.find_all("tbody")[0]), "lxml")
    # print(vids_table_soup)
  except IndexError:
    return vids
    pass
  else:
    # print(vids_table_soup)

    for vids_row_li in vids_table_soup.find_all("tr", ["pl-video", "yt-uix-tile"]):
      # print(vids_row_li)
      title = vids_row_li.get("data-title")
      # print(title)
      if not(vchannel_data_api.title_checker(filter_phrases, title)):
        vids_row_soup = BeautifulSoup(str(vids_row_li), "lxml")
        href = vids_row_soup.find("a", "pl-video-title-link").get("href")
        vid_id = href.split("?v=")[1].split("&")[0]
        # print(href, vid_id)

        if not (vid_id in exclude_yt_vid_ids) \
          and not (smart_downloader.in_cache('youtube', vid_id)):
            ydl_dict = ydl_api_extended.ydl_get_dict(vid_id)
            # print(ydl_dict)

            if ydl_dict['formats']:
              ydl_dict['title'] = title   # since ydl is unable to extract video titles
              if ydl_dict['pub_date'] >= since_date:
                if not short_form:
                  print(vid_id, ydl_dict['title'])
                  vids.append(ydl_dict)
                else:
                  if ydl_dict['duration'] < 1200:
                    print(vid_id, ydl_dict['title'])
                    vids.append(ydl_dict)
              else:
                break
      # print(vids)
      return vids

# print(ydl_playlist_spider_obsolete("https://www.youtube.com/playlist?list=UUvJJ_dzjViJCoLf5uKUTwoA", datetime.date(2021, 2, 10)))


'''
def ydl_etcg_spider(since_date):
  vids = []

  playlist_url = vchannel_data_api.lookup_by_source('etcg')['data_source']
  playlist_whole_soup = BeautifulSoup(requests.get(playlist_url).text, "lxml")
  vids_table_soup = BeautifulSoup(str(playlist_whole_soup.find_all("tbody")[0]), "lxml")
  # print(vids_table_soup)

  for vids_row_li in vids_table_soup.find_all("tr", ["pl-video", "yt-uix-tile"]):
    vids_row_soup = BeautifulSoup(str(vids_row_li),"lxml")
    href = vids_row_soup.find("a", "pl-video-title-link").get("href")
    vid_id = href.split("?v=")[1].split("&")[0]

    ydl_dict = ydl_api_extended.ydl_get_dict(vid_id)
    # print(ydl_dict)
    title = ydl_dict['title']

    cache_title = filename_tools.make_valid(filename_tools.prep_comp_string(title))
    # print(vid_id, comp_title)

    if not (vid_id in exclude_yt_vid_ids) \
        and not (smart_downloader.in_cache('youtube', vid_id)):
      if smart_downloader.etcg_title_in_cache(cache_title):
        smart_downloader.sync_etcg_cache(cache_title, 'youtube', vid_id)

      else:
        if ydl_dict['formats'] and (ydl_dict['pub_date'] >= since_date):
          print(vid_id, ydl_dict['title'])
          vids.append(ydl_dict)
        else:
          break

  playlist_url = vchannel_data_api.lookup_by_source('etcg-dailyblob')['data_source']
  playlist_whole_soup = BeautifulSoup(requests.get(playlist_url).text, "lxml")
  vids_table_soup = BeautifulSoup(str(playlist_whole_soup.find_all("tbody")[0]), "lxml")
  # print(vids_table_soup)

  for vids_row_li in vids_table_soup.find_all("tr", ["pl-video", "yt-uix-tile"]):
    vids_row_soup = BeautifulSoup(str(vids_row_li), "lxml")
    href = vids_row_soup.find("a", "pl-video-title-link").get("href")
    vid_id = href.split("?v=")[1].split("&")[0]

    ydl_dict = ydl_api_extended.ydl_get_dict(vid_id)
    # print(ydl_dict)
    title = ydl_dict['title']

    cache_title = filename_tools.make_valid(filename_tools.prep_comp_string(title))
    # print(vid_id, comp_title)

    if not (vid_id in exclude_yt_vid_ids) \
      and not (smart_downloader.in_cache('youtube', vid_id)):
      if smart_downloader.etcg_title_in_cache(cache_title):
        smart_downloader.sync_etcg_cache(cache_title, 'youtube', vid_id)

      else:
        if ydl_dict['formats'] and (ydl_dict['pub_date'] >= since_date):
          print(vid_id, ydl_dict['title'])
          vids.append(ydl_dict)
        else:
          break

  return vids
'''


'''
def ydl_etcg_spider_old(playlist_url, since_date):
  vids = []

  contents_d = playlist_to_contents_dict(playlist_url)

  # List of videos rendered in playlist
  for vid in contents_d:
    vid_id = vid["playlistVideoRenderer"]["videoId"]
    # print("videoID: ", vid_id)
    title = vid["playlistVideoRenderer"]["title"]["simpleText"]
    # print("title: ", title)
    # print("index: ", vid["playlistVideoRenderer"]["index"]["simpleText"])
    # print("length: ", vid["playlistVideoRenderer"]["lengthSeconds"])
    vid_url = "https://www.youtube.com/watch?v=" + vid_id

    if not (vid_id in exclude_yt_vid_ids) and not (smart_downloader.in_cache('youtube', vid_id)):
      vid_contents_d = vid_to_contents_dict(vid_url)
      # print(vid_contents_d)

      vid_title = vid_contents_d["title"]["runs"][0]["text"]
      vid_dateText = vid_contents_d["dateText"]["simpleText"]
      # print(vid_title, vid_dateText)

      # if 'Premieres' doesn't appear in date_slot_str
      if vid_dateText.find(ydl_api_extended.verbage6) == -1:
        # print(vid_id, title)

        ydl_dict = ydl_api_extended.ydl_get_dict(vid_id)
        # print(ydl_dict)
        title = ydl_dict['title']

        cache_title = filename_tools.make_valid(filename_tools.prep_comp_string(title))
        # print(vid_id, comp_title)

        if ydl_dict['formats'] and (ydl_dict['pub_date'] >= since_date):
          if smart_downloader.etcg_title_in_cache(cache_title):
            smart_downloader.sync_etcg_cache(cache_title, 'youtube', vid_id)
          else:
            print(vid_id, ydl_dict['title'], vid_dateText)
            vids.append(ydl_dict)
            # print("Appended: ", ydl_dict)
        else:
          break

  # print(vids)
  return vids

# print(ydl_etcg_spider(datetime.date(2020, 5, 1)))
# print(ydl_playlist_spider("https://youtube.com/playlist?list=UUvJJ_dzjViJCoLf5uKUTwoA", datetime.date(2019, 4, 14)))
# print(ydl_etcg_spider(vchannel_data_api.lookup_by_source('etcg')['data_source'], datetime.date(2019, 9, 10)))

def ydl_download_etcg_old(playlist_name, since_date, format=ydl_api_extended.yt_formats['labels']['low_res']):
  d = vchannel_data_api.lookup_by_source(playlist_name)

  try:
    vids = ydl_etcg_spider_old(d['data_source'], since_date)
    print(playlist_name, vids)
  except TypeError:
    pass
  else:
    for vids_d in vids:
      vid_name = filename_tools.make_valid(vids_d['title'])
      datestr = vids_d['upload_date']

      request_url = ''
      for vid_format in vids_d['formats']:
        if vid_format[ydl_api_extended.yt_formats['criteria']] == format:
          request_url = vid_format['url']

      print("URL: " + request_url)
      udl_alg.download_video(request_url, datestr + ' - ' + vid_name, d['destination_path'], ext=".mp4")
      smart_downloader.append_vid('youtube', vids_d['vid_id'])

      # ETCG Vid Cache JSON
      cache_title = filename_tools.make_valid(filename_tools.prep_comp_string(vids_d['title']))

      smart_downloader.sync_etcg_cache(cache_title, 'youtube', vids_d['vid_id'])
'''

