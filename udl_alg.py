'''
Name: udl_alg.py (Universal Downloader)

What:
Basic downloader algorithm based on OS
'''


import os
import filename_tools
import subprocess
import urllib.request


def win_cmd(source, target):
  if source.endswith(".m3u8'"):
    subprocess.run(
      ['ffmpeg', '-i', source, '-c', 'copy', target],
      shell=True
    )
  elif source.endswith(".mp4'"):
    subprocess.run(f"powershell (New-Object system.net.webclient).DownloadFile({source}, {target})", shell=True)


def download_video(url, name, path, ext=".mp4"):
  filename = name + ext
  full_filename = path + filename_tools.shrink_whitespace(filename)
  print("Downloading:", name)

  # For Windows OS
  if os.name == 'nt':
    if url.endswith('.m3u8'):
      if os.path.isfile(full_filename):
        if os.stat(full_filename).st_size >= 2000:
          pass
        else:
          subprocess.run(
            ['ffmpeg', '-i', url, '-c', 'copy', full_filename],
            shell=True
          )
      else:
        subprocess.run(
          ['ffmpeg', '-i', url, '-c', 'copy', full_filename],
          shell=True
        )

    else:
      ps_url = "'" + filename_tools.prep_ps_url(url) + "'"
      print(ps_url)
      ps_filename = "'" + filename_tools.prep_ps_filename(full_filename) + "'"

      if os.path.isfile(full_filename):
        if os.stat(full_filename).st_size >= 2000:
          pass
        else:
          win_cmd(ps_url, ps_filename)

      else:
        win_cmd(ps_url, ps_filename)

  # For Linux OS
  elif os.name == 'posix':
    sh_url = "'" + url + "'"
    sh_filename = '"' + full_filename + '"'

    if os.path.isfile(full_filename):
      if os.stat(full_filename).st_size >= 2000:
        pass
      else:
        subprocess.run("wget -O {} {}".format(sh_filename, sh_url), shell=True)

    else:
      subprocess.run("wget -O {} {}".format(sh_filename, sh_url), shell=True)


# print("'" + filename_tools.prep_ps_url(url) + "'")
# print("'" + full_filename + "'")
# subprocess.run("powershell Invoke-WebRequest {} -OutFile {}".format("'" + filename_tools.prep_ps_url(url) + "'", "'" + full_filename + "'"), shell=True)

def podcast_downloader(url, full_path):
  sh_url = "'" + url + "'"
  sh_fullpath = '"' + full_path + '"'


  if os.path.isfile(full_path):
    if os.stat(full_path).st_size >= 2000:
      pass
    else:
      # For Windows OS
      if os.name == 'nt':
        urllib.request.urlretrieve(url, full_path)

      # For Linux
      elif os.name == 'posix':
        subprocess.run("wget -O {} {}".format(sh_fullpath, sh_url), shell=True)
  else:
    # For Windows OS
    if os.name == 'nt':
      urllib.request.urlretrieve(url, full_path)

    # For Linux
    elif os.name == 'posix':
      subprocess.run("wget -O {} {}".format(sh_fullpath, sh_url), shell=True)

  if os.stat(full_path).st_size < 2000:
    podcast_downloader(url, full_path)

