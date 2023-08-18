'''
Name: vchannel_data_api.py
Better names:
  cloud env
  ext env

What:
Define video channel/playlist (cloud) variables and preferences
'''


import local_env
import filename_tools
import re

vchannels_dict = {
  'platforms': [
    {'id': 'youtube',
     'url_prefix': 'https://www.youtube.com/playlist?list=',
     'url_suffix': '',
     'low_res_label': '360p - mp4',
     'high_res_label': '720p - mp4',
     'long_form': '144p - 3gp'},
    {'id': 'espn',
     'url_prefix': 'http://m.espn.com/general/video?cid=',
     'url_suffix': '&page=all',
     'low_res_label': '360p - mp4',
     'high_res_label': '720p - mp4',
     'long_form': '144p - mp4'}
  ],
  'sources': [
    {'id': 'bible-project', 'platform': 'youtube', 'list_id': 'UUeqnFRVfjy5R5ZUR92IZlpg',
     'playlists': [
       {'title': 'How to Read the Bible', 'list_id': 'PLH0Szn1yYNedn4FbBMMtOlGN-BPLQ54IH'},
       {'title': 'Word Studies', 'list_id': 'PLH0Szn1yYNeclOdfwWBawnNT5ZkGFHxBf'},
       {'title': 'The Wisdom Series', 'list_id': 'PLH0Szn1yYNeeKPNIy7YXjO3MGD8h8ifhr'},
       {'title': 'The Gospel Series', 'list_id': 'PLH0Szn1yYNec6O3ZOZzAMb2WW2abJwzZ-'},
       {'title': 'Biblical Themes', 'list_id': 'PLH0Szn1yYNec-HZjVHooeb4BSDSeHhEoh'},
       {'title': 'NT', 'list_id': 'PLH0Szn1yYNecanpQqdixWAm3zHdhY2kPR'},
       {'title': 'OT', 'list_id': 'PLH0Szn1yYNeeVFodkI9J_WEATHQCwRZ0u'},
       {'title': 'The Torah Series', 'list_id': 'PLH0Szn1yYNee8aedW_5aCpnzkxnV7VQ3K'}
    ]},
    {'id': 'bible-project-mandarin', 'platform': 'youtube', 'list_id': 'UUBx_1SLtNfZEHx2HCWWTDVQ',
     'playlists': [
       {'title': 'How to Read the Bible', 'list_id': 'PLE-R0uydm0uPJ2M2BZ4dFYuWBjf-34pMX'},
       {'title': 'Read Scripture OT', 'list_id': 'PLE-R0uydm0uN0xKD3tw0aheiQojlf1JB1'},
       {'title': 'Read Scripture NT', 'list_id': 'PLE-R0uydm0uMPY7cu-kuEkcPHAM0M9Cby'},
       {'title': 'The Torah Series', 'list_id': 'PLE-R0uydm0uPCscWNPsa-6ycASTfZcOeI'},
       {'title': 'The Wisdom Series', 'list_id': 'PLE-R0uydm0uOVfcnpg1DcmzbEisLSJXEo'},
       {'title': 'Biblical Themes', 'list_id': 'PLE-R0uydm0uMw9xIFD5G5xe1uyb71o7m8'},
       {'title': 'Luke Mini Series', 'list_id': 'PLE-R0uydm0uM5h3RO2ToKLbxz9Jg5rCK9'}
     ]},
    {'id': 'bible-project-canto', 'platform': 'youtube', 'list_id': 'UUoq4W0bLI28a17qPtZ5x1pQ',
     'playlists': [
       {'title': 'Read Scripture OT', 'list_id': 'PLf7Dzn7kHAxWPyOzcvJiIEY5NIxpo2gs-'},
       {'title': 'Read Scripture NT', 'list_id': 'PLf7Dzn7kHAxWNyvLs4zl6w1ybrdTKBnU_'},
       {'title': 'Biblical Themes', 'list_id': 'PLf7Dzn7kHAxVHv2xDRYXsapSq7ewGCBJB'}
     ]},
    {'id': 'ptx', 'platform': 'youtube', 'list_id': 'UUmv1CLT6ZcFdTJMHxaR9XeA',
     'playlists': [
       {'title': 'Christmas Is Here', 'list_id': 'PLU_mcNMHvximh1Z_LdrUU2r2_05PlISBM'},
       {'title': 'Christmas Deluxe', 'list_id': 'OLAK5uy_nslslALKFTvA73yKcSmOjIKmDV5jPCv3I'},
       {'title': 'PTXMas', 'list_id': 'PLIdPxD0zhZDMgFWjBnrkNywOYYfbbnvEw'}
    ]},
    {'id': 'coding-arena', 'platform': 'youtube', 'list_id': 'UUv5hBnMW_k3ZGRE1a0cVNAw',
     'playlists': [
       # Done: {'title': 'MS Cert Prep', 'list_id': 'PL084kyX5OrJQgjFgZztG4B6Z7cagQXnTz'},
       # Done: {'title': 'ASP.NET Core', 'list_id': 'PL084kyX5OrJTmEY4xAfw11sZZCfs7KSwR'},
       # Done: {'title': 'HTML5 CSS3', 'list_id': 'PL084kyX5OrJTGLiXr5AZiz-qN5garskgJ'},
       # Done: {'title': 'XAML HTML5', 'list_id': 'PLsrZV8shpwjOdW96Pz2N2V9Sdcaww6yfC'},
       # Done: {'title': 'HTML5 JS CSS3', 'list_id': 'PLsrZV8shpwjN25T9ANfzYoH5siVbdSrFQ'},
       # Done: {'title': 'MS PS', 'list_id': 'PLsrZV8shpwjMXYBmmGodMMQV86xsSz1si'},
       # Done: {'title': 'MS AD', 'list_id': 'PLsrZV8shpwjOtIz4LFKFQ6uoCt7RowYUZ'},
       # Done: {'title': '98-365 WS Admin Fundamentals', 'list_id': 'PLsrZV8shpwjMmq9hw_vlpDswWWw8jGJnZ'},
       # Done: {'title': '98-366 Networking Fundamentals', 'list_id': 'PLsrZV8shpwjMLQZSfvlusAfngXpr58O-A'},
       # Done: {'title': 'C# Fundamentals for Beginners', 'list_id': 'PLsrZV8shpwjMkG96rkKLdNiX02S5LPIqS'},
       # Done: {'title': 'C#', 'list_id': 'PL084kyX5OrJRkOHEBO7RdQ3WEVSiTsXvQ'},
       # Done: {'title': 'ASP.NET MVC', 'list_id': 'PL084kyX5OrJQjjf3Sm0BtLrJvN4Ga6IVg'},
       # Done: {'title': 'Java 9 for Beginners', 'list_id': 'PL084kyX5OrJStm54Dx9qaxAnmIEFbdrPV'},
       # Done: {'title': 'JAMF 100', 'list_id': 'PLlxHm_Px-Ie3OmPPwlFliyBKLGU_dbqtq'},
       # Done: {'title': 'Java', 'list_id': 'PL084kyX5OrJR7j4I0NlwY4xxfw9xIqcCa'},
       # Done: {'title': 'AngularJS 2.0', 'list_id': 'PL084kyX5OrJRyxtsViWcv7kgLs1Nvnggq'},
       # Done: {'title': 'Android Dev', 'list_id': 'PL084kyX5OrJQ3lk1yBuDGvpNupSfwsi0M'},
       # Done: {'title': 'C++', 'list_id': 'PL084kyX5OrJSrSHxyr5qyC--y0AVJOFIE'},
       # Done: {'title': 'JSON with C#', 'list_id': 'PL084kyX5OrJTko_wZHGxDUUTkYVAWsR1p'},
       # Done: {'title': 'MEAN Stack Jumpstart', 'list_id': 'PLsrZV8shpwjPuVqMcqAsxTHgGm8lW15nN'},
       # Done: {'title': 'Web API Design Jumpstart', 'list_id': 'PLsrZV8shpwjOeFL9a3P6_lnXbM1ztbnPA'},
       # Done: {'title': 'iOS App Dev', 'list_id': 'PL084kyX5OrJQimH-63H-0Cd6MqhTFl_V9'},
       #
       #
       # {'title': 'MongoDB', 'list_id': 'PL084kyX5OrJRODRuD_2frAMlhRIurKCv5'},
       # {'title': 'Python in VS', 'list_id': 'PL084kyX5OrJRTKdaIkyx0hPy3O0F1LHHS'},
       # {'title': 'Node.js in VS', 'list_id': 'PL084kyX5OrJRa820Z6dYg5Xr5dJVr92ZH'},
       #
       #
       # {'title': 'MS Cert Prep', 'list_id': 'PL084kyX5OrJQgjFgZztG4B6Z7cagQXnTz'},
       # {'title': 'MS Cert Prep', 'list_id': 'PL084kyX5OrJQgjFgZztG4B6Z7cagQXnTz'},
       # {'title': 'MS Cert Prep', 'list_id': 'PL084kyX5OrJQgjFgZztG4B6Z7cagQXnTz'},
       # {'title': 'MS Cert Prep', 'list_id': 'PL084kyX5OrJQgjFgZztG4B6Z7cagQXnTz'},
       # {'title': 'MS Cert Prep', 'list_id': 'PL084kyX5OrJQgjFgZztG4B6Z7cagQXnTz'},
       # {'title': 'MS Cert Prep', 'list_id': 'PL084kyX5OrJQgjFgZztG4B6Z7cagQXnTz'},
       # {'title': 'Xamarin', 'list_id': 'PL084kyX5OrJRl94c3Yt98_tmunGOKr3Kb'}
    ]},
    {'id': 'cnbc',
     'platform': 'youtube',
     'list_id': 'UUvJJ_dzjViJCoLf5uKUTwoA',
     'upload_url': 'https://www.youtube.com/c/CNBC/videos'},
    {'id': 'cnet',
     'platform': 'youtube',
     'list_id': 'UUOmcA3f_RrH6b9NmcNa4tdg',
     'upload_url': 'https://www.youtube.com/c/CNET/videos'},
    {'id': 'mkbhd',
     'platform': 'youtube',
     'list_id': 'UUBJycsmduvYEL83R_U4JriQ',
     'upload_url': 'https://www.youtube.com/c/mkbhd/videos'},
    {'id': 'verge',
     'platform': 'youtube',
     'list_id': 'UUddiUEpeqJcYeBxX1IVBKvQ',
     'upload_url': 'https://www.youtube.com/c/TheVerge/videos'},
    {'id': 'espn-yt',
     'platform': 'youtube',
     'list_id': 'UUiWLfSweyRNmLpgEHekhoAg',
     'upload_url': 'https://www.youtube.com/c/ESPN/videos'},
    {'id': 'america-uncovered',
     'platform': 'youtube',
     'list_id': 'UU_7vFlErTHxVD-IFNB-BFCg',
     'upload_url': 'https://www.youtube.com/c/AmericaUncovered/videos'},
    {'id': 'china-uncensored',
     'platform': 'youtube',
     'list_id': 'UUgFP46yVT-GG4o1TgXn-04Q',
     'upload_url': 'https://www.youtube.com/c/ChinaUncensored/videos'},
    {'id': 'computerphile',
     'platform': 'youtube',
     'list_id': 'UU9-y-6csu5WGm29I7JiwpnA',
     'upload_url': 'https://www.youtube.com/user/Computerphile/videos'},
    {'id': 'numberphile',
     'platform': 'youtube',
     'list_id': 'UUoxcjq-8xIDTYp3uz647V5A',
     'upload_url': 'https://www.youtube.com/user/numberphile/videos'},
    {'id': 'numberphile2',
     'platform': 'youtube',
     'list_id': 'UUyp1gCHZJU_fGWFf2rtMkCg',
     'upload_url': 'https://www.youtube.com/c/numberphile2/videos'},
    {'id': 'healthcare-triage',
     'platform': 'youtube',
     'list_id': 'UUabaQPYxxKepWUsEVQMT4Kw',
     'upload_url': 'https://www.youtube.com/c/healthcaretriage/videos'},
    {'id': 'khanacademy',
     'platform': 'youtube',
     'list_id': 'UU4a-Gbdw7vOaccHmFo40b9g',
     'upload_url': 'https://www.youtube.com/c/khanacademy/videos'},
    {'id': 'tom-scott',
     'platform': 'youtube',
     'list_id': 'UUBa659QWEk1AI4Tg--mrJ2A',
     'upload_url': 'https://www.youtube.com/c/TomScottGo/videos'},
    {'id': 'tasty-japan',
     'platform': 'youtube',
     'list_id': 'UUilGprjH_UBgR5vLVXPff3Q',
     'upload_url': 'https://www.youtube.com/c/TastyJapan/videos'},
    {'id': 'etcg',
     'platform': 'youtube',
     'list_id': 'UUD4EOyXKjfDUhCI6jlOZZYQ',
     'upload_url': 'https://www.youtube.com/c/Elithecomputerguypage/videos'},
    {'id': 'etcg-dailyblob',
     'platform': 'youtube',
     'list_id': 'UUJRhK2b92UpOr4LBCWVaFDw',
     'upload_url': 'https://www.youtube.com/c/TheThingoftheName/videos'},
    {'id': 'threat-wire',
     'platform': 'youtube',
     'list_id': 'PLW5y1tjAOzI0Sx4UU2fncEwQ9BQLr5Vlu',
     'upload_url': 'https://www.youtube.com/c/hak5/videos'},
    {'id': 'nfl-official',
     'platform': 'youtube',
     'playlists_url': 'https://www.youtube.com/c/NFL/playlists',
     'list_id': 'UUDVYQ4Zhbm3S2dlz7P1GBDg',
     'upload_url': 'https://www.youtube.com/c/NFL/videos?view=0&sort=dd&shelf_id=430'},
    {'id': 'android-developers', 'platform': 'youtube', 'list_id': 'UUVHFbqXqoYvEWM1Ddxl0QDg'},
    {'id': 'ms-courses', 'platform': 'youtube', 'list_id': 'UUJ31x5A6zIdHF5tJhjftyiA'},
    {'id': 'etcg-fn', 'platform': 'youtube', 'list_id': 'UULhuVUeaOfQLRctfj4OiahQ'},
    {'id': 'etcg-gsn', 'platform': 'youtube', 'list_id': 'UUzNfNFQWaO-fA2qWAeXMJ-A'},
    {'id': 'cnbc-longform', 'platform': 'youtube', 'list_id': 'UUvJJ_dzjViJCoLf5uKUTwoA'},
    {'id': 'mobilegeeks', 'platform': 'youtube', 'list_id': 'UU0GhiZR9zyPorNmoWyPClrQ'},
    {'id': 'yuezhi', 'platform': 'youtube', 'list_id': 'UUvGkex9MrqV2d4wah9JuANg'},
    {'id': 'crazy-canton', 'platform': 'youtube', 'list_id': 'UUz_Ceq3mxLeTdCriXUDz72Q'},
    {'id': 'fox-wc2018', 'platform': 'youtube', 'list_id': 'UUooTLkxcpnTNx6vfOovfBFA'},
    {'id': 'latest', 'platform': 'espn', 'list_id': '2378529'},
    {'id': 'mlb', 'platform': 'espn', 'list_id': '2521705'},
    {'id': 'nba', 'platform': 'espn', 'list_id': '2459788'},
    {'id': 'nfl', 'platform': 'espn', 'list_id': '2459789'},
    {'id': 'nhl', 'platform': 'espn', 'list_id': '2459791'},
    {'id': 'tennis', 'platform': 'espn', 'list_id': '2491545'}
  ],
  'destinations': [
    {'id': 'bible-project', 'path': local_env.bible_project_path},
    {'id': 'bible-project-canto', 'path': local_env.bible_project_canto_path},
    {'id': 'bible-project-mandarin', 'path': local_env.bible_project_mandarin_path},
    {'id': 'ptx', 'path': local_env.ptx_music_path},
    {'id': 'cnet', 'path': local_env.rolling_video_path},
    {'id': 'verge', 'path': local_env.rolling_video_path},
    {'id': 'cnbc', 'path': local_env.cnbc_path},
    {'id': 'cnbc-longform', 'path': local_env.cnbc_path + local_env.cnbc_longform_path},
    {'id': 'mobilegeeks', 'path': local_env.rolling_video_path},
    {'id': 'threat-wire', 'path': local_env.rolling_video_path},
    {'id': 'china-uncensored', 'path': local_env.rolling_video_path},
    {'id': 'america-uncovered', 'path': local_env.rolling_video_path},
    {'id': 'android-developers', 'path': local_env.android_dev_path},
    {'id': 'mkbhd', 'path': local_env.rolling_video_path},
    {'id': 'healthcare-triage', 'path': local_env.ht_path},
    {'id': 'tom-scott', 'path': local_env.rolling_video_path},
    {'id': 'ms-courses', 'path': local_env.tech_training_path},
    {'id': 'coding-arena', 'path': local_env.tech_training_path},
    {'id': 'computerphile', 'path': local_env.computerphile_path},
    {'id': 'numberphile', 'path': local_env.numberphile_path},
    {'id': 'numberphile2', 'path': local_env.numberphile_path},
    {'id': 'etcg', 'path': local_env.etcg_longform_path},
    {'id': 'etcg-dailyblob', 'path': local_env.etcg_longform_path},
    {'id': 'etcg-fn', 'path': local_env.etcg_longform_path},
    {'id': 'etcg-gsn', 'path': local_env.etcg_longform_path},
    {'id': 'yuezhi', 'path': local_env.rolling_video_path},
    {'id': 'crazy-canton', 'path': local_env.rolling_video_path},
    {'id': 'nfl-official', 'path': local_env.nfl_hi_res_path},
    {'id': 'khanacademy', 'path': local_env.khanacademy_hi_res_path},
    {'id': 'fox-wc2018', 'path': local_env.espn_video_path},
    {'id': 'espn-yt', 'path': local_env.espn_video_path},
    {'id': 'tasty-japan', 'path': local_env.recipes_path},
    {'id': 'latest', 'path': local_env.espn_video_path},
    {'id': 'mlb', 'path': local_env.espn_video_path},
    {'id': 'nba', 'path': local_env.espn_video_path},
    {'id': 'nfl', 'path': local_env.espn_video_path},
    {'id': 'nhl', 'path': local_env.espn_video_path},
    {'id': 'tennis', 'path': local_env.espn_video_path}
  ]
}

def lookup_by_source(source):
  d = {}
  platform_id = ''
  # data_source = ''
  list_id = ''
  upload_url = ''
  dest_path = ''
  playlists_url = ''
  for i in vchannels_dict['sources']:
    if i['id'] == source:
      platform_id = i['platform']
      list_id = i['list_id']
      if platform_id == 'youtube':
        upload_url = i['upload_url']
      # data_source = i['data_source']
      try:
        if i['playlists_url']:
          playlists_url = i['playlists_url']
      except KeyError:
        playlists_url = ''

  for i in vchannels_dict['destinations']:
    if i['id'] == source:
      dest_path = local_env.video_root + i['path']

  for i in vchannels_dict['platforms']:
    if i['id'] == platform_id:
      d = {
        'id': source,
        'platform': platform_id,
        'data_source': i['url_prefix'] + list_id + i['url_suffix'],
        'upload_url': upload_url,
        'playlists_url': playlists_url,
        'destination_path': dest_path,
        'low_res_label': i['low_res_label'],
        'high_res_label': i['high_res_label'],
        'long_form': i['long_form']
      }
  return d

# print(lookup_by_source('mkbhd'))


def lookup_playlists_by_source(source):
  d = {}
  platform_id = ''
  list_id = ''
  # data_source = ''
  playlists = []
  dest_path = ''
  for i in vchannels_dict['sources']:
    if i['id'] == source:
      platform_id = i['platform']
      # data_source = i['data_source']
      list_id = i['list_id']
      playlists = i['playlists']

  for i in vchannels_dict['destinations']:
    if i['id'] == source:
      dest_path = local_env.video_root + i['path']

  for i in vchannels_dict['platforms']:
    if i['id'] == platform_id:
      d = {
        'id': source,
        'platform': platform_id,
        'list_id': list_id,
        'playlists': playlists,
        'destination_path': dest_path,
        'url_prefix': i['url_prefix'],
        'url_suffix': i['url_suffix'],
        'low_res_label': i['low_res_label'],
        'high_res_label': i['high_res_label'],
        'long_form': i['long_form']
      }

  for playlist in d['playlists']:
    playlist['data_source'] = d['url_prefix'] + playlist['list_id'] + d['url_suffix']

  return d

# print(lookup_playlists_by_source('bible-project'))

etcg_ids = ['etcg', 'etcg-dailyblob']
cuau_ids = ['china-uncensored', 'america-uncovered']

podcasts = [
  {'pod_id': 2386164,
   'details': {
     'name': 'baseball tonight', 'xml_url': 'https://feeds.megaphone.fm/ESP1723897648'
  }},
  {'pod_id': 2544461,
   'details': {
     'name': 'fantasy focus baseball', 'xml_url': 'http://www.espn.com/espnradio/feeds/rss/podcast.xml?id=2544461'
  }},
  {'pod_id': 9545077,
   'details': {
     'name': 'jalen and jacoby', 'xml_url': 'http://www.espn.com/espnradio/feeds/rss/podcast.xml?id=9545077'
  }},
  {'pod_id': 27852002,
   'details': {
     'name': 'espn daily', 'xml_url': 'https://feeds.megaphone.fm/ESP8348692127'
   }},
  {'details': {'name': 'security now', 'xml_url': 'http://feeds.twit.tv/sn.xml'}},
  {'details': {'name': 'aom', 'xml_url': 'http://feeds.feedburner.com/artofmanlinesspodcast'}},
  {'details': {'name': 'klaw show', 'xml_url': 'https://feeds.simplecast.com/L15G3UJb', 'cdn_url': True}},
  {'details': {'name': 'behind the braves', 'xml_url': 'http://mlb.mlb.com/feed/podcast/behind_the_braves_rss.xml'}},
  {'details': {'name': 'executive access', 'xml_url': 'http://mlb.mlb.com/feed/podcast/executive_access_rss.xml', 'cdn_url': True}},
  {'details': {'name': 'morning lineup', 'xml_url': 'http://mlb.mlb.com/feed/podcast/newsmakers_rss.xml'}},
  {'details': {'name': 'statcast podcast', 'xml_url': 'http://mlb.mlb.com/feed/podcast/statcast_podcast_rss.xml'}},
  {'details': {'name': 'intentional talk', 'xml_url': 'http://mlb.mlb.com/feed/podcast/c17429946.xml', 'cdn_url': False}},
  {'details': {'name': 'play ball', 'xml_url': 'http://mlb.mlb.com/feed/podcast/mlbn_play_ball_rss.xml', 'cdn_url': False}}
]

def lookup_xml_url_by_name(pod_name):
  for d in podcasts:
    if d['details']['name'] == pod_name:
      return d['details']['xml_url']


def lookup_cdn_by_pod_name(pod_name):
  for d in podcasts:
    if d['details']['name'] == pod_name:
      return d['details']['cdn_url']


#ESPN Filter
espn_phrases = ['UFC',
  'Esports',
  'WWE',
  'ESPN FC',
  'Cricinfo',
  'Manziel',
  'DraftExpress',
  'MMA',
  'Pro Football Hall of Fame',
  'College GameDay',
  'Stephen A.',
  'First Take',
  'NBA Preseason Highlights',
  'NBA Highlights',
  'NBA Sound',
  'NBA on ESPN',
  '2020 NBA Playoff',
  'Tournament Highlights',
  'CFB Highlights',
  'College Basketball Highlights',
  'Prep Highlights',
  'Australian Open Highlights',
  'XFL Highlights',
  'XFL on ESPN',
  'Ligue 1 Highlights',
  'US Open Highlights',
  'Bracket',
  'CBB',
  'The Ocho',
  'Senior Night',
  'senior night',
  'SeniorNight',
  'Ariel & The Bad Guy',
  'Wrestlemania',
  'WrestleMaina',
  'Body by Jake',
  'Top Rank',
  'DraftExpress',
  'Boxing',
  'Ariel Helwani',
  'Helwani',
  'McGregor',
  'Khabib',
]


def title_checker(phrases, title):
  ans = False

  for phrase in phrases:
    ans = ans or not(re.search(phrase, title) == None)
  # print('Running title_checker on ' + title, ans)

  return ans


#CNET Filter
cnet_phrases = ['EP. ',
  'Ep. ',
  'ep. ',
  'live coverage',
  'Stream Economy',
  'stream economy',
  'Westworld',
  'CNET UK podcast',
  'CNET UK Podcast',
  'Fortt Knox',
  'Cracking Open',
]



#CNBC Filter
cnbc_phrases = ['live price updates', 'White House', 'Press Briefing']


#Aggregated filter phrases
agg_filters = [
  {'creator_id': 'cnet',
   'filter_phrases': [
     'EP. ',
     'Ep. ',
     'ep. ',
     'live coverage',
     'Stream Economy',
     'stream economy',
     'Westworld',
     'CNET UK podcast',
     'CNET UK Podcast',
     'Fortt Knox',
     'Cracking Open'
   ]},
  {'creator_id': 'cnbc',
   'filter_phrases': [
     'live price updates',
     'White House',
     'Press Briefing'
   ]},
  {'creator_id': 'espn-yt',
   'filter_phrases': [
     'UFC',
     'Esports',
     'WWE',
     'ESPN FC',
     'Cricinfo',
     'Manziel',
     'DraftExpress',
     'MMA',
     'Pro Football Hall of Fame',
     'College GameDay',
     'Stephen A.',
     'First Take',
     'NBA Preseason Highlights',
     'NBA Highlights',
     'NBA Sound',
     'NBA on ESPN',
     '2020 NBA Playoff',
     'Tournament Highlights',
     'CFB Highlights',
     'College Basketball Highlights',
     'Prep Highlights',
     'Australian Open Highlights',
     'XFL Highlights',
     'XFL on ESPN',
     'Ligue 1 Highlights',
     'US Open Highlights',
     'Bracket',
     'CBB',
     'The Ocho',
     'Senior Night',
     'senior night',
     'SeniorNight',
     'Ariel & The Bad Guy',
     'Wrestlemania',
     'WrestleMaina',
     'Body by Jake',
     'Top Rank',
     'DraftExpress',
     'Boxing',
     'Ariel Helwani',
     'Helwani',
     'McGregor',
     'Khabib'
   ]},
  {'creator_id': 'khanacademy',
   'filter_phrases': [
     'Khan Stories: ',
     'Khan Acaedmy Live!',
     'Homeroom with Sal'
   ]},
  {'creator_id': 'tom-scott',
   'filter_phrases': [
     'Citation Needed'
   ]}
]


def lookup_filter_by_creator(creator_id):
  ans = []

  for filters in agg_filters:
    if filters['creator_id'] == creator_id:
      ans = filters['filter_phrases']
      break

  return ans

# print(lookup_filter_by_creator("cnbc"))


def identity(str):
  return filename_tools.make_valid(str)

def cnet_naming_rules(title):
  ans = ''

  if title.endswith(" Watch This Space"):
    ans = 'WTS ' + filename_tools.make_valid(title).split(' Watch This Space')[0]
  elif title.endswith(" What the Future"):
    ans = 'WTF ' + filename_tools.make_valid(title).split(' What the Future')[0]
  else:
    ans = filename_tools.make_valid(title)

  return ans


def au_naming_rules(title):
  return 'AU ' + filename_tools.make_valid(title)


def cu_naming_rules(title):
  return 'CU ' + filename_tools.make_valid(title)


def tw_naming_rules(title):
  return 'TW ' + filename_tools.make_valid(title)


def ht_naming_rules(title):
  return 'HT ' + filename_tools.make_valid(title)


def ts_naming_rules(title):
  return 'TS ' + filename_tools.make_valid(title)


def mlb_it_naming_rules(pod_date):
  return 'IT ' + pod_date.__format__('%Y%m%d')


def mlb_pb_naming_rules(pod_date):
  return 'PB ' + pod_date.__format__('%Y%m%d')


def espn_bbtn_naming_rules(pod_date):
  return pod_date.__format__('%Y%m%d') + '-BBTN'


def espn_daily_naming_rules(pod_date):
  return pod_date.__format__('%Y%m%d') + '-DAILY'


def espn_ffb_naming_rules(pod_date):
  return pod_date.__format__('%Y%m%d') + '-FFB'


def espn_jnj_naming_rules(pod_date):
  return pod_date.__format__('%Y%m%d') + '-JNJ'


def klaw_show_naming_rules(pod_date):
  return pod_date.__format__('%Y%m%d') + '-KLAW'


def bpd_naming_rules(pod_date):
  return pod_date.__format__('%Y%m%d') + '-BPD'


agg_naming_rules = [
  {'creator_id': 'cnet', 'naming_rule': cnet_naming_rules},
  {'creator_id': 'healthcare-triage', 'naming_rule': ht_naming_rules},
  {'creator_id': 'tom-scott', 'naming_rule': ts_naming_rules},
  {'creator_id': 'america-uncovered', 'naming_rule': au_naming_rules},
  {'creator_id': 'china-uncensored', 'naming_rule': cu_naming_rules},
  {'creator_id': 'threat-wire', 'naming_rule': tw_naming_rules},
  {'creator_id': 'baseball tonight', 'naming_rule': espn_bbtn_naming_rules},
  {'creator_id': 'espn daily', 'naming_rule': espn_daily_naming_rules},
  {'creator_id': 'fantasy focus baseball', 'naming_rule': espn_ffb_naming_rules},
  {'creator_id': 'jalen and jacoby', 'naming_rule': espn_jnj_naming_rules},
  {'creator_id': 'klaw show', 'naming_rule': klaw_show_naming_rules},
  {'creator_id': 'statcast podcast', 'naming_rule': bpd_naming_rules},
  {'creator_id': 'intentional talk', 'naming_rule': mlb_it_naming_rules},
  {'creator_id': 'play ball', 'naming_rule': mlb_pb_naming_rules}
]

def lookup_naming_rules_by_creator(creator_id):
  ans = identity

  for rules in agg_naming_rules:
    if rules['creator_id'] == creator_id:
      ans = rules['naming_rule']
      break

  return ans

