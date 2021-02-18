from django.http import JsonResponse
from django.shortcuts import render

# Create your views here.

# current index view
from fbdl4u.forms import LinkInsert, LinkAjax
from fbdl4u.helper import cook_fb_url, is_fb_url_valid, get_video_dict_fb


def fbdl_front_view(request):
    link_form = LinkInsert()
    context = {
        'file_url': '',
        'form': link_form
    }
    return render(request, 'front_index2.html', context)


# first ajax post
def ajax_post_fb_link(request):
    if request.is_ajax and request.method == "POST":
        form = LinkAjax(request.POST)
        if form.is_valid():
            link_cleaned = form.cleaned_data.get('link')
            cooked_url = cook_fb_url(link_cleaned)
            if is_fb_url_valid(cooked_url):

                vids_dict = get_video_dict_fb(cooked_url)
                return JsonResponse(vids_dict, status=200)
            else:
                return JsonResponse({'error': 'Error! Please enter a correct facebook video link.'}, status=500)
        else:
            # some form errors occurred.
            return JsonResponse({"error": form.errors}, status=400)

    # some error occurred
    return JsonResponse({"error": "some error occurred! try again."}, status=400)


# second ajax post
def ajax_post_format_dl(request):
    if request.is_ajax and request.method == "POST":
        form = LinkInsert(request.POST)
        if form.is_valid():
            vid_format_cleaned = form.cleaned_data.get('video_format')
            if vid_format_cleaned != '':
                link2 = form.cleaned_data.get('link2')
                if link2 != '':
                    cooked_url = cook_fb_url(link2)
                    if is_fb_url_valid(cooked_url):
                        vids_dict = get_video_dict_fb(cooked_url)
                        if vid_format_cleaned == 'HD':
                            if vids_dict.get('HD'):
                                return JsonResponse({"dl_url": vids_dict.get('HD'), "unique_id": 123,
                                                     'format': 'HD', 'device': 'iOS'}, status=200)
                        elif vid_format_cleaned == 'SD':
                            if vids_dict.get('SD'):
                                return JsonResponse({"dl_url": vids_dict.get('SD'), "unique_id": 123,
                                                     'format': 'SD/Low Resolution', 'device': 'iOS'}, status=200)

                        return JsonResponse({"dl_url": '#', "unique_id": 123,
                                             'format': 'sd'}, status=200)
                    else:
                        return JsonResponse({"error": 'Please enter youtube video URL.'}, status=400)
            return JsonResponse({"error": "some error occurred! try again."}, status=200)
        else:
            # some form errors occurred.
            return JsonResponse({"error": form.errors}, status=400)

    # some error occurred
    return JsonResponse({"error": "some error occurred! try again."}, status=400)
