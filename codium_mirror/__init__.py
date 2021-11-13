
import os
import platform
import re
import subprocess
import sys

__version__ = '0.0.1'
__appauthor__ = 'larryw3i & Contributors'

base_path = os.path.dirname(os.path.abspath(__file__))
bash_path = os.path.join(base_path, 'codium_mirror.bash')
mirrors_path = os.path.join(base_path, 'codium.mirrors')

sys_argv = sys.argv[1:]
sys_argv = ' '.join(sys_argv)


mirror = re.findall(r'--mirror=(\S*)', sys_argv)[0] or 'TUNA'


def get_architecture():

    # default
    architecture = subprocess.check_output('uname -m', shell=True)\
        .decode().strip()
    return architecture in ['x86_64'] and 'amd64' or ''


architecture = get_architecture()


def get_mirror_url():
    mirrors = open(mirrors_path).read().split('\n')
    mirrors = [m for m in mirrors if len(m) > 0]
    for m in mirrors:
        m_splits = m.split(' ')
        if m_splits[0] == mirror:
            return m_splits[-1]
    return mirrors[0].split(' ')[-1]


mirror_url = get_mirror_url()


def get_pkgs():

    # default
    html = subprocess.check_output('curl ' + mirror_url, shell=True)
    links = re.findall(r'href="(\S*)"', html.decode())
    links = [l for l in links if '/' not in l]
    return links


pkgs = get_pkgs()


def get_os_release():
    os_release = subprocess.check_output('cat /etc/os-release', shell=True)
    os_release = re.findall(r'ID_LIKE=(\S*)\n', os_release.decode())[0]
    return os_release in ['debian'] and 'deb' or ''


os_release = get_os_release()


def get_installation_sh(os_release, pkg):

    # default
    if os_release in ['deb']:
        return \
            f'curl {mirror_url+pkg} --output {pkg}; ' +\
            f'sudo dpkg --install {pkg}; ' +\
            f'rm -rf {pkg}'


def run():
    for p in pkgs:
        if os_release in p and architecture in p and p.endswith('.deb'):
            os.system(get_installation_sh(os_release, p))


print('\n',
      'base_path', '\n\t', base_path, '\n',
      'bash_path', '\n\t', bash_path, '\n',
      'sys_argv', '\n\t', sys_argv, '\n',
      'get_architecture', '\n\t', get_architecture(), '\n',
      'get_mirror', '\n\t', get_mirror_url(), '\n',
      'mirror', '\n\t', mirror, '\n',
      'get_os_release', '\n\t', get_os_release(), '\n')

