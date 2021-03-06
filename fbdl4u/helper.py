import os
import re
import sys
import ffmpeg

from django.core.files import File
from django.utils.encoding import force_text
from pip._vendor import requests

from fbdl.settings import BASE_DIR


def get_valid_filename_to_uri(s):
    """
    Returns the given string converted to a string that can be used for a clean
    filename. Specifically, leading and trailing spaces are removed; other
    spaces are converted to underscores; and anything that is not a unicode
    alphanumeric, dash, underscore, or dot, is removed.
    get_valid_filename("john's portrait in 2004.jpg")
    'johns_portrait_in_2004.jpg'
    """
    s = force_text(s).strip().replace(' ', '_')
    return re.sub(r'(?u)[^-\w.]', '', s)


def get_clean_filename(s):
    """
    returns clean readable name.
    """
    s = force_text(s).strip().replace('_', ' ')
    return re.sub(r'(?u)[^-\w.]', ' ', s)


# New for fb-dl
def get_video_dict_fb(link, only_src=False):
    sdvideo_url = ''
    hdvideo_url = ''
    title = ''
    try:
        html = requests.get(link).content.decode('utf-8')
        sdvideo_url = re.search('sd_src:"(.+?)"', html)[1]
        hdvideo_url = re.search('hd_src:"(.+?)"', html)[1]
        title = re.search('<title.*?>(.+?)</title>', html)[1]
    except:
        pass
    vid_dict = {}
    if sdvideo_url:
        vid_dict.update({'SD': sdvideo_url})
    if hdvideo_url:
        vid_dict.update({'HD': hdvideo_url})
    if title:
        if not only_src:
            x = get_valid_filename_to_uri(title)
            vid_dict.update({'title': x})
    return vid_dict


def get_client_ip(request):
    ip = ''
    try:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[-1].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')
    except:
        pass
    return ip


def get_user_agent(request):
    ua = ''
    try:
        ua = request.META['HTTP_USER_AGENT']
    except:
        pass

    return ua


def is_fb_url_valid(url):
    if url.startswith('https://www.facebook.com/') or url.startswith('https://fb.watch/'):
        return True
    else:
        return False


# fixing url
def cook_fb_url(url):
    if url.startswith('https://www.facebook.com/') or url.startswith('https://fb.watch/'):
        return url
    elif url.startswith('facebook.com/'):
        return 'https://www.' + url
    elif url.startswith('www.facebook.com/'):
        return 'https://' + url
    elif url.startswith('fb.watch/'):
        return 'https://' + url
    else:
        return url


def convert_aud_mp4_to_mp3(aud_url='', name='', to_save=''):
    # print('name:', name)
    # input_audio = ffmpeg.input(aud_url)
    if '.mp4' in name:
        name = name.replace('.mp4', '.mp3')
    _output = to_save + '/' + name

    filename = _output
    if not os.path.exists(os.path.dirname(filename)):
        try:
            os.makedirs(os.path.dirname(filename))
        except OSError as exc:  # Guard against race condition
            pass

    '''ffmpeg.output(
        input_audio,
        _output,
    ).run(overwrite_output=True)
    # working
    '''

    '''(ffmpeg
     .input(input_audio)
     .output(_output)
     .overwrite_output()
     .run()
     )'''

    (ffmpeg
     .input(aud_url)
     .output(_output)
     .overwrite_output()
     .run()
     )

    return _output


# downloading video from remote host
def get_aud(url='', name=''):
    """url = 'https://www.facebook.com/...'
    r = requests.get(url, allow_redirects=True)
    open('facebook.ico', 'wb').write(r.content)"""

    if url:
        '''iterate through all links in video_links  
        and download them one by one'''

        # obtain filename by splitting url and getting
        # last string
        # file_name = url.split('/')[-1]
        to_save_folder = str(BASE_DIR / 'media/audio/temp')
        print('tosave', to_save_folder)
        abs_path = to_save_folder + '/' + name+'.mp4'

        # print("Downloading file:%s" % name)

        # create response object
        r = requests.get(url, stream=True)

        filename = abs_path
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc:  # Guard against race condition
                pass

        # download started
        with open(abs_path, 'wb') as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)

        # print("%s downloaded!\n" % abs_path)
        aud_name = name+'.mp3'
        convert_aud_mp4_to_mp3(aud_url=abs_path, name=aud_name, to_save=str(BASE_DIR / 'media/audio/deliver'))
        to_ret_dict = {
            'abs_path': 'media/audio/deliver/' + aud_name,
            'name': aud_name,
            'content_type': 'audio/mpeg',
            'format': 'mp3 (128kbps)'
        }
        return to_ret_dict


# not working :(
def get_file_name_from_req(url=''):
    file_name = ''
    if url:
        r = requests.get(url)
        d = r.headers.get('content-disposition')
        file_name = re.findall("filename=(.+)", d)[0]
    return file_name
