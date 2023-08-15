'''
Name: podcast_alg.py

What:
Algorithm for podcasts
'''


import datetime
import datetime_tools
import urllib.request
import requests
from bs4 import BeautifulSoup
import re
import local_env
import udl_alg
import vchannel_data_api


# RTHK Morning News
def rthk_downloader(since_date):
  # d = datetime.date.today()
  hk_upload_time = datetime_tools.convert_time(8-8)

  d = datetime.date(year=hk_upload_time.year, month=hk_upload_time.month, day=hk_upload_time.day)

  while d >= since_date:
    rthk_single_download(d)
    d = datetime_tools.day_before(d)


def rthk_single_download(date):
  # url = "http://archive.rthk.hk/mp3/radio/archive/radio1/morningnews/mp3/" + date.__format__('%Y%m%d') + ".mp3"

  url = "http://archive.rthk.hk/mp3/radio/archive/radio1/morningnews/m4a/" + date.__format__('%Y%m%d') + ".m4a"
  path = local_env.podcast_root + local_env.rthk_pod_path

  # filename = date.__format__('%Y%m%d') + ".mp3"

  filename = date.__format__('%Y%m%d') + ".m4a"

  try:
    print("Downloading:", filename)
    udl_alg.podcast_downloader(url, path + filename)
  except urllib.error.HTTPError:
    pass


#rthk_downloader(datetime.date(2017, 10, 12))


# ESPN Podcasts

def espn_podcenter_downloader(pod_name, since_date):
  #d = datetime.date.today()
  path = local_env.podcast_root + local_env.espn_pod_path
  xml_url = vchannel_data_api.lookup_xml_url_by_name(pod_name)

  source_code = requests.get(xml_url)
  plain_text = source_code.text
  # print(plain_text)

  whole_soup = BeautifulSoup(plain_text, 'lxml')
  urls = []
  for item in whole_soup.find_all("item"):
    title = item.find("title").string
    # print(title)
    pod_date = item.find("pubdate").string[:16]
    pod_datetime = datetime.datetime.strptime(pod_date, '%a, %d %b %Y')

    pod_day = pod_datetime.day
    pod_month = pod_datetime.month
    pod_year = pod_datetime.year
    # print(pod_date, pod_year, pod_month, pod_day)

    if not(re.match('^Scoreboard', title)) and not(re.match('^SCOREBOARD', title)):
      dl_url = item.find("enclosure").get("url")
      # print(dl_url)

      filename = vchannel_data_api.lookup_naming_rules_by_creator(pod_name)(pod_datetime) + ".mp3"
      if datetime.date(pod_year, pod_month, pod_day) >= since_date:
        urls.append({'url': dl_url, 'filename': filename})

  for l in urls:
    print("Downloading:", l['filename'])

    udl_alg.podcast_downloader(l['url'], path + l['filename'])


#print(requests.get(vchannel_data_api.lookup_xml_url_by_name('baseball tonight')).text)
#espn_podcenter_downloader('fantasy focus baseball', datetime.date(2017, 10, 6))
#espn_podcenter_downloader('baseball tonight', datetime.date(2017, 10, 11))
#espn_podcenter_downloader('jalen and jacoby', datetime.date(2017, 10, 11))


# The Keith Law Show Podcasts

def klaw_show_downloader(since_date):
  path = local_env.podcast_root + local_env.espn_pod_path
  xml_url = vchannel_data_api.lookup_xml_url_by_name('klaw show')

  source_code = requests.get(xml_url)
  plain_text = source_code.text
  # print(plain_text)

  whole_soup = BeautifulSoup(plain_text, 'lxml')
  urls = []
  for item in whole_soup.find_all("item"):
    pod_date = item.find("pubdate").string[:-15]
    # print(pod_date)
    pod_datetime = datetime.datetime.strptime(pod_date, '%a, %d %b %Y')

    pod_day = pod_datetime.day
    pod_month = pod_datetime.month
    pod_year = pod_datetime.year
    # print(pod_date, pod_year, pod_month, pod_day)

    dl_url = item.find("enclosure").get("url")
    cdn_url = requests.get(dl_url).url.split("?")[0]
    # print(cdn_url)
    # filename = urllib.request.unquote(cdn_url.split("/")[-1])
    filename = vchannel_data_api.lookup_naming_rules_by_creator('klaw show')(pod_datetime) + ".mp3"

    if datetime.date(pod_year, pod_month, pod_day) >= since_date:
      urls.append({'url': dl_url, 'filename': filename})
    else:
      break

  for l in urls:
    print("Downloading:", l['filename'])

    udl_alg.podcast_downloader(l['url'], path + l['filename'])


# MLB.com Podcasts

def mlb_podcast_downloader(pod_name, since_date):
  path = local_env.podcast_root + local_env.espn_pod_path
  xml_url = vchannel_data_api.lookup_xml_url_by_name(pod_name)

  source_code = requests.get(xml_url)
  plain_text = source_code.text
  #print(plain_text)

  whole_soup = BeautifulSoup(plain_text, 'lxml')
  urls = []
  for item in whole_soup.find_all("item"):
    pod_date = item.find("pubdate").string[:16]
    pod_datetime = datetime.datetime.strptime(pod_date, '%a, %d %b %Y')

    pod_day = pod_datetime.day
    pod_month = pod_datetime.month
    pod_year = pod_datetime.year
    # print(pod_date, pod_year, pod_month, pod_day)

    dl_url = item.find("enclosure").get("url")
    cdn_url = requests.get(dl_url).url
    # print(cdn_url)
    # filename = urllib.request.unquote(cdn_url.split("/")[-1])
    filename = vchannel_data_api.lookup_naming_rules_by_creator(pod_name)(pod_datetime) + ".mp3"


    if datetime.date(pod_year, pod_month, pod_day) >= since_date:
      urls.append({'url': dl_url, 'filename': filename})
    else:
      break

  for l in urls:
    print("Downloading:", l['filename'])

    udl_alg.podcast_downloader(l['url'], path + l['filename'])


def mlb_it_downloader(since_date):
  path = local_env.video_root + local_env.espn_video_path
  xml_url = vchannel_data_api.lookup_xml_url_by_name('intentional talk')

  source_code = requests.get(xml_url)
  plain_text = source_code.text
  #print(plain_text)

  whole_soup = BeautifulSoup(plain_text, 'lxml')
  urls = []
  for item in whole_soup.find_all("item"):
    pod_date = item.find("pubdate").string[:16]
    pod_datetime = datetime.datetime.strptime(pod_date, '%a, %d %b %Y')

    pod_day = pod_datetime.day
    pod_month = pod_datetime.month
    pod_year = pod_datetime.year
    # print(pod_date, pod_year, pod_month, pod_day)

    dl_url = item.find("enclosure").get("url")
    cdn_url = requests.get(dl_url).url
    # print(cdn_url)
    filename = "IT " + pod_datetime.__format__('%Y%m%d') + ".m4v"


    if datetime.date(pod_year, pod_month, pod_day) >= since_date:
      urls.append({'url': dl_url, 'filename': filename})
    else:
      break

  for l in urls:
    print("Downloading:", l['filename'])

    udl_alg.podcast_downloader(l['url'], path + l['filename'])



def mlb_vpodcast_downloader(pod_name, since_date):
  path = local_env.video_root + local_env.mlb_video_path
  xml_url = vchannel_data_api.lookup_xml_url_by_name(pod_name)

  source_code = requests.get(xml_url)
  plain_text = source_code.text
  # print(plain_text)

  whole_soup = BeautifulSoup(plain_text, 'lxml')
  urls = []
  for item in whole_soup.find_all("item"):
    pod_date = item.find("pubdate").string[:16].strip()
    # print(pod_date)
    pod_datetime = datetime.datetime.strptime(pod_date, '%a, %d %b %Y')

    pod_day = pod_datetime.day
    pod_month = pod_datetime.month
    pod_year = pod_datetime.year
    # print(pod_date, pod_year, pod_month, pod_day)

    dl_url = item.find("enclosure").get("url")

    if vchannel_data_api.lookup_cdn_by_pod_name(pod_name):
      dl_url = requests.get(dl_url).url

    # print(dl_url)

    filename = re.split('\/',dl_url)[-1]

    '''
    if pod_name == "intentional talk":
        filename = vchannel_data_api.lookup_naming_rules_by_creator(pod_name)(pod_datetime) + ".m4v"
    '''

    if datetime.date(pod_year, pod_month, pod_day) >= since_date:
      urls.append({'url': dl_url, 'filename': filename})
    else:
      break

  for l in urls:
    print("Downloading:", l['filename'])

    udl_alg.podcast_downloader(l['url'], path + l['filename'])



# Security Now Podcast

#print(vchannel_data_api.lookup_xml_url_by_name('security now'))
#print(requests.get(lookup_sn_xml('security now')).text)

def sn_downloader(pod_name, since_date):
  path = local_env.podcast_root + local_env.sn_pod_path
  xml_url = vchannel_data_api.lookup_xml_url_by_name(pod_name)

  source_code = requests.get(xml_url)
  plain_text = source_code.text
  #print(plain_text)

  whole_soup = BeautifulSoup(plain_text, 'lxml')
  urls = []
  for item in whole_soup.find_all("item"):
    dl_url = item.find("enclosure").get("url")
    #print(dl_url)
    filename = re.split('\/',dl_url)[-1]
    #print(filename)
    pod_date = item.find("pubdate").string[:16]
    pod_datetime = datetime.datetime.strptime(pod_date, '%a, %d %b %Y')

    pod_day = pod_datetime.day
    pod_month = pod_datetime.month
    pod_year = pod_datetime.year
    #print(pod_date, pod_year, pod_month, pod_day)

    if datetime.date(pod_year, pod_month, pod_day) >= since_date:
      urls.append({'url': dl_url, 'filename': filename})

  for l in urls:
    print("Downloading:", l['filename'])

    udl_alg.podcast_downloader(l['url'], path + l['filename'])

#sn_downloader('security now', datetime.date(2017, 10, 12))


# Art of Manliness Podcast

def aom_downloader(pod_name, since_date):
  path = local_env.podcast_root + local_env.aom_pod_path
  xml_url = vchannel_data_api.lookup_xml_url_by_name(pod_name)

  source_code = requests.get(xml_url)
  plain_text = source_code.text
  # print(plain_text)

  whole_soup = BeautifulSoup(plain_text, 'lxml')
  urls = []
  for item in whole_soup.find_all("item"):
    # print(item)
    pod_date = item.find("pubdate").string[:16]
    pod_datetime = datetime.datetime.strptime(pod_date, '%a, %d %b %Y')

    pod_day = pod_datetime.day
    pod_month = pod_datetime.month
    pod_year = pod_datetime.year
    # print(pod_date, pod_year, pod_month, pod_day)

    description = item.find("description").text
    # print(description)

    guest_name = ""
    guest_name_candidate = ""

    if description.find('y guests ') != -1:
      try:
        guest_name_candidate = description.split('names are ')[1].split('.')[0].split(',')[0]
        # print(guest_name_candidate)
      except IndexError:
        break
      guest_name = guest_name_candidate
    else:
      try:
        guest_name_candidate = description.split('name is ')[1].split('�and')[0].split(' and')[0].split('.')[0].split(',')[0]
        # print(guest_name_candidate)
      except IndexError:
        break

      a_texts = []

      for a in item.find_all("a"):
        a_texts.append(a.text)
      # print(a_texts)

      if guest_name_candidate in a_texts:
        guest_name = guest_name_candidate
      else:
        print(item)

    dl_url = item.find("enclosure").get("url")
    # print(dl_url)
    episode_num = item.find("itunes:episode").text
    # print(episode_num)

    cdn_url = requests.get(dl_url).url
    # print(cdn_url)
    cdn_filename = urllib.request.unquote(cdn_url.split("/")[-1])
    # print(cdn_filename)

    filename = "#" + str(episode_num) + " " + guest_name + ".mp3"
    # print(filename)

    if datetime.date(pod_year, pod_month, pod_day) >= since_date:
      urls.append({'url': dl_url, 'filename': filename})
    else:
      break

  for l in urls:
    print("Downloading:", l['filename'])

    udl_alg.podcast_downloader(l['url'], path + l['filename'])

# aom_downloader('aom', datetime.date(2019, 6, 10))
# print(requests.get(vchannel_data_api.lookup_xml_url_by_name('aom')).text)
