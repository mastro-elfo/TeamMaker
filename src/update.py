
from requests import get
from string import ascii_letters, punctuation
from os.path import join, abspath, expanduser
from os import sep, listdir
from shutil import unpack_archive, copytree, rmtree

def check_update(version):
    try:
        ret = get('https://api.github.com/repos/mastro-elfo/TeamMaker/releases/latest')
        json = ret.json()
        ver = get_version(json['tag_name'])
        act = get_version(version)
        return ver > act, json
        # return True, {'tarball_url': 'https://api.github.com/repos/mastro-elfo/TeamMaker/tarball/v1.1'}
    except Exception as e:
        # print('Error', str(e))
        return False, None

def download_update(url):
    try:
        ret = get(url)
        with open(join(abspath(sep), 'tmp', 'teammaker.tar.gz'), 'wb') as fp:
            fp.write(ret.content)
        return True, ''
    except Exception as e:
        return False, str(e)

def extract_update():
    try:
        unpack_archive(join((abspath(sep)), 'tmp', 'teammaker.tar.gz'), join((abspath(sep)), 'tmp', 'teammaker'))
        return True, ''
    except Exception as e:
        return False, str(e)

def install_contents():
    try:
        # TODO: with python3.8 `copytree` has `dirs_exist_ok=True`
        # https://docs.python.org/3/library/shutil.html#shutil.copytree
        pack_dir = listdir(join((abspath(sep)), 'tmp', 'teammaker'))[0]
        rmtree(join(expanduser('~'), '.local', 'share', 'TeamMaker'), ignore_errors = True)
        copytree(join((abspath(sep)), 'tmp', 'teammaker', pack_dir), join(expanduser('~'), '.local', 'share', 'TeamMaker'))
        return True, ''
    except Exception as e:
        return False, str(e)

def get_version(tag):
    return tuple([int(x)  for x in tag.translate(str.maketrans('', '', ascii_letters + punctuation.replace('.', ''))).split('.')])
