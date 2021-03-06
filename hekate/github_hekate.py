from github import Github
import urllib.request
import tempfile
import shutil
import re
import os

class GithubHekate():
  def __init__(self, github_token=""):
    if github_token == '' and os.environ.get('GITHUB_TOKEN') != '':
      github_token = os.environ["GITHUB_TOKEN"]
    else:
      raise ValueError('could not find GITHUB_TOKEN')

    self.g = Github(github_token)

  def get_hekate(self):
    repo = self.g.get_repo("CTCaer/hekate")
    return repo

  def list_hekate_releases(self):
    hekate = self.get_hekate()
    releases = hekate.get_releases()
    return releases

  def list_named_hekate_releases(self):
    releases = []

    for release in self.list_hekate_releases():
      match = re.search('^v([.\d]*)', release.tag_name)
      
      if match:
        releases.append({ 'id': release.id, 'name': match.group(1) })

    # https://stackoverflow.com/a/2574090/5332177
    releases.sort(key=lambda s: [int(u) for u in s['name'].split('.')], reverse=True)

    return releases
  
  def get_release_assets(self, id):
    hekate = self.get_hekate()
    release = hekate.get_release(id)
    return release.get_assets()

  def get_archive_asset(self, id):
    assets = self.get_release_assets(id)

    for asset in assets:
      if ".zip" in asset.name:
        return asset
    
    return None

  def get_download_archive(self, id):
    archive_asset = self.get_archive_asset(id)
    
    with urllib.request.urlopen(archive_asset.browser_download_url) as response:
        with tempfile.NamedTemporaryFile(delete=False) as tmp_file:
          shutil.copyfileobj(response, tmp_file)
          return tmp_file.name
