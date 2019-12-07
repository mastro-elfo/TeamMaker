
from requests import get
from string import ascii_letters, punctuation

def check_update(version):
    try:
        ret = get('https://api.github.com/repos/mastro-elfo/TeamMaker/releases/latest')
        rel = ret.json()
        ver = get_version(rel['tag_name'])
        act = get_version(version)
        return ver > act
    except Exception as e:
        print('Error', str(e))
        return False

def download_update():
    return False

def extract_update():
    return False

def get_version(tag):
    return tuple([int(x)  for x in tag.translate(str.maketrans('', '', ascii_letters + punctuation.replace('.', ''))).split('.')])
