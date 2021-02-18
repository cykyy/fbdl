import os
import re
import sys

from django.core.files import File
from django.utils.encoding import force_text
from pip._vendor import requests


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


'''def get_video_formats_list(link):
    # https://www.youtube.com/watch?v=PEuGRCqc8fQ
    try:
        yt_obj = YouTube(link)
        yt = yt_obj.streams.filter(file_extension='mp4')  # , only_video=True
        # return yt
        vid_list = []
        for vid in yt:
            vid_list.append(vid)
        # print(vid_list[0].itag)

        return vid_list
    except Exception as e:
        print(e)'''


def get_video_dict(vid_list):
    vid_dict = {}
    p1080 = False
    p720 = False
    p480 = False
    p360 = False
    p240 = False
    p144 = False
    mp3 = False

    for vid in vid_list:
        if vid.resolution is not None:
            if vid.resolution == '1080p':
                if not p1080:
                    vid_dict.update({vid.resolution: vid.itag})
                    p1080 = True
            elif vid.resolution == '720p':
                if vid.is_progressive:
                    vid_dict.update({vid.resolution: vid.itag})
                    p720 = True
                    continue
                if not p720:
                    vid_dict.update({vid.resolution: vid.itag})
                    p720 = True
            elif vid.resolution == '480p':
                if not p480:
                    vid_dict.update({vid.resolution: vid.itag})
                    p480 = True
            elif vid.resolution == '360p':
                if vid.is_progressive:
                    vid_dict.update({vid.resolution: vid.itag})
                    p360 = True
                    continue
                if not p360:
                    vid_dict.update({vid.resolution: vid.itag})
            elif vid.resolution == '240p':
                if not p240:
                    vid_dict.update({vid.resolution: vid.itag})
                    p240 = True
            elif vid.resolution == '144p':
                if not p144:
                    vid_dict.update({vid.resolution: vid.itag})
                    p144 = True
        if vid.itag == 140:
            if not mp3:
                vid_dict.update({'mp3 (128kbps)': vid.itag})
                mp3 = True

    return vid_dict


# New for fb-dl
def get_video_dict_fb(link):
    sdvideo_url = ''
    hdvideo_url = ''
    try:
        html = requests.get(link).content.decode('utf-8')
        sdvideo_url = re.search('sd_src:"(.+?)"', html)[1]
        hdvideo_url = re.search('hd_src:"(.+?)"', html)[1]
    except:
        pass

    vid_dict = {
        'HD': hdvideo_url,
        'SD': sdvideo_url
    }
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
    # print('is_fb_url_val', url)
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
