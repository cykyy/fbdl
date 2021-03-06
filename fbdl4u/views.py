from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.

# current index view
from fbdl4u.forms import LinkInsert, LinkAjax, ContactForm
from fbdl4u.helper import cook_fb_url, is_fb_url_valid, get_video_dict_fb, get_aud, get_file_name_from_req, \
    get_user_agent, get_client_ip
from fbdl4u.models import Job


def fbdl_front_view(request):
    # get_aud()
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

                vids_dict = get_video_dict_fb(cooked_url, only_src=True)

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
                                Job.objects.create(name=vids_dict.get('title'), facebook=vids_dict.get('HD'),
                                                   resolution="HD", format="Video", abs_path="remote",
                                                   user_agent=get_user_agent(request), ip_addr=get_client_ip(request))
                                return JsonResponse({"dl_url": vids_dict.get('HD'), "unique_id": 123,
                                                     'format': 'HD', 'device': 'iOS'}, status=200)
                        elif vid_format_cleaned == 'SD':
                            if vids_dict.get('SD'):
                                Job.objects.create(name=vids_dict.get('title'), facebook=vids_dict.get('SD'),
                                                   resolution="SD", format="Video", abs_path="remote",
                                                   user_agent=get_user_agent(request), ip_addr=get_client_ip(request))
                                return JsonResponse({"dl_url": vids_dict.get('SD'), "unique_id": 123,
                                                     'format': 'SD/Low Resolution', 'device': 'iOS'}, status=200)
                        elif vid_format_cleaned == 'Audio':  # if requested for audio!;
                            if vids_dict:
                                # if HD available then convert hd video to audio
                                name = vids_dict.get('title')
                                fb_url = ''
                                if vids_dict.get('HD'):
                                    fb_url = vids_dict.get('HD')
                                else:
                                    fb_url = vids_dict.get('SD')

                                aud_dict = get_aud(url=fb_url, name=name)
                                Job.objects.create(name=vids_dict.get('title'), facebook=fb_url,
                                                   resolution="Audio", format="Audio",
                                                   abs_path=str(aud_dict.get('abs_path')),
                                                   user_agent=get_user_agent(request), ip_addr=get_client_ip(request))

                                return JsonResponse({"dl_url": aud_dict.get('abs_path'), "unique_id": 125,
                                                     'format': 'Mp3 128Kbps', 'device': 'iOS'}, status=200)

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


def privacy_policy_view(request):
    return render(request, 'privacy.html', {})


def terms_view(request):
    return render(request, 'terms.html', {})


def contact_us_view(request):
    my_form = ContactForm()
    if request.method == 'POST':
        my_form = ContactForm(request.POST)
        if my_form.is_valid():
            my_form.save()

            messages.success(request, 'Message sent successfully!')
            return redirect('fbdl:contact')
        else:
            messages.error(request, 'Failed to sent message, try again!')
            return redirect('fbdl:contact')
    context = {
        'form': my_form
    }
    return render(request, 'contact_us.html', context)
