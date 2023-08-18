'''
Name: content_downloader.py
Better names:
  Media downloaders
  daily downloaders


What:
Run downloader commands
'''


import datetime
import datetime_tools
import podcast_alg
import ydl_alg
import gc
import ydl_api_extended

since_date = datetime.date(2023, 8, 15)
nfl_season = 2022
nfl_week = 1

gc.collect()

print(datetime.datetime.now())

'''
Download podcasts
'''

# podcast_alg.aom_downloader('aom', since_date)
# podcast_alg.espn_podcenter_downloader('baseball tonight', since_date)
# podcast_alg.espn_podcenter_downloader('espn daily', since_date)
# podcast_alg.klaw_show_downloader(since_date)
# podcast_alg.mlb_podcast_downloader('behind the braves', datetime_tools.day_before(since_date))
# podcast_alg.mlb_podcast_downloader('statcast podcast', datetime_tools.day_before(since_date))
# podcast_alg.sn_downloader('security now', datetime_tools.day_before(since_date))
# podcast_alg.rthk_downloader(since_date)
# podcast_alg.rthk_downloader(datetime_tools.day_after(since_date))




'''
Using youtube_dl library
'''
def ydl_pkg(since_date):


  gc.collect()
  ydl_alg.ydl_download_playlist('cnbc', since_date, short_form=False)
  ydl_alg.ydl_download_playlist('cnet', since_date)
  ydl_alg.ydl_download_playlist('mkbhd', since_date, short_form=False)
  ydl_alg.ydl_download_playlist('verge', since_date, short_form=False)


  gc.collect()
  ydl_alg.ydl_download_playlist('america-uncovered', since_date, short_form=False)
  ydl_alg.ydl_download_playlist('china-uncensored', since_date, short_form=False)


  gc.collect()
  ydl_alg.ydl_download_playlist('computerphile', since_date, short_form=False)
  ydl_alg.ydl_download_playlist('numberphile', since_date, short_form=False)
  ydl_alg.ydl_download_playlist('numberphile2', since_date, short_form=False)


  gc.collect()
  ydl_alg.ydl_download_playlist('healthcare-triage', since_date)
  ydl_alg.ydl_download_playlist('khanacademy', since_date, ydl_api_extended.yt_formats['labels']['hi_res'])
  ydl_alg.ydl_download_playlist('tom-scott', since_date, short_form=False)


  gc.collect()
  ydl_alg.ydl_download_playlist('tasty-japan', datetime_tools.day_before(since_date), short_form=False)


def ydl_espn_pkg():

  ydl_alg.ydl_download_espn_group('latest')
  # ydl_alg.ydl_download_espn_group('nfl')
  ydl_alg.ydl_download_espn_group('nba')
  ydl_alg.ydl_download_espn_group('mlb')
  # ydl_alg.ydl_download_espn_group('tennis')

  # ydl_alg.ydl_download_playlist('espn-yt', since_date)
  # podcast_alg.espn_podcenter_downloader('baseball tonight', datetime_tools.day_after(since_date))
  # podcast_alg.espn_podcenter_downloader('jalen and jacoby', since_date)
  # podcast_alg.mlb_vpodcast_downloader('intentional talk', since_date)
  # podcast_alg.mlb_vpodcast_downloader('intentional talk', datetime_tools.day_before(since_date))
  # podcast_alg.mlb_vpodcast_downloader('play ball', datetime_tools.day_before(since_date))


def ydl_bible_project_pkg():

  ydl_alg.ydl_download_bible_project()
  ydl_alg.ydl_download_bible_project_canto()
  ydl_alg.ydl_download_bible_project_mandarin()





# ydl_alg.ydl_download_single_playlist("https://www.youtube.com/playlist?list=PLaD4FvsFdarS6zpoEmgW_4V_B606vI8gf", "JIRA Software Webinars")





'''
ydl_alg.ydl_single_video("https://www.youtube.com/watch?v=5yJsVE3FzBg", 'healthcare-triage')
ydl_alg.ydl_single_video("https://www.youtube.com/watch?v=27PMklYzXm4", 'healthcare-triage')
ydl_alg.ydl_single_video("https://www.youtube.com/watch?v=AgQ5Gm7gjlE", 'china-uncensored')
ydl_alg.ydl_single_video("https://www.youtube.com/watch?v=QHxrxtXGiMA", 'cnbc')
ydl_alg.ydl_single_video("https://www.youtube.com/watch?v=1jBPG2fe6XQ", 'mkbhd')
ydl_alg.ydl_single_video("https://www.youtube.com/watch?v=sOrxNvaGgLI", 'mkbhd')
ydl_alg.ydl_single_video("https://www.youtube.com/watch?v=wzU46BiYh2o", 'mkbhd')
ydl_alg.ydl_single_video("https://www.youtube.com/watch?v=CTtANYNhbLU", 'mkbhd')
ydl_alg.ydl_single_video("https://www.youtube.com/watch?v=Z-lq-z5KM2c", 'mkbhd')
ydl_alg.ydl_single_video("https://www.youtube.com/watch?v=gzEynheMp4E", 'mkbhd')
ydl_alg.ydl_single_video("https://www.youtube.com/watch?v=JxFNFUD-hUc", 'mkbhd')
ydl_alg.ydl_single_video("https://www.youtube.com/watch?v=HUY_e-y4HHc", 'mkbhd')
ydl_alg.ydl_single_video("https://www.youtube.com/watch?v=NluVlZCToSg", 'mkbhd', format=ydl_api_extended.yt_formats['labels']['hi_res'])
ydl_alg.ydl_single_video("https://www.youtube.com/watch?v=GOXEADdM0ZI", 'mkbhd', format=ydl_api_extended.yt_formats['labels']['hi_res'])
ydl_alg.ydl_single_video("https://www.youtube.com/watch?v=LBr-blQxIm4", 'mkbhd', format=ydl_api_extended.yt_formats['labels']['hi_res'])
ydl_alg.ydl_single_video("https://www.youtube.com/watch?v=WA4vkrRCXOY", 'numberphile')
ydl_alg.ydl_single_video("https://www.youtube.com/watch?v=bRkUGqsz6SI", 'computerphile', format=ydl_api_extended.yt_formats['labels']['hi_res'])
ydl_alg.ydl_single_video("https://www.youtube.com/watch?v=LoVTGQiSzUU", 'tasty-japan', format=ydl_api_extended.yt_formats['labels']['hi_res'])
ydl_alg.ydl_single_video("https://www.youtube.com/watch?v=_m5nefx8aDM", 'khanacademy')
'''



gc.collect()
# ydl_alg.ydl_download_nfl_highlights(nfl_week, nfl_season)


gc.collect()
# ydl_pkg(since_date)


gc.collect()
# ydl_alg.ydl_download_etcg_bundle(datetime_tools.day_before(datetime_tools.day_before(since_date)))


gc.collect()
# ydl_alg.ydl_download_playlist('threat-wire', datetime_tools.day_before(datetime_tools.day_before(datetime_tools.day_before(since_date))))


gc.collect()
# ydl_bible_project_pkg()


gc.collect()
ydl_espn_pkg()


print(datetime.datetime.now())

gc.collect()


