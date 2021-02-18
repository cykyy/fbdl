from django import forms


class LinkInsert(forms.Form):
    link = forms.CharField(max_length=256, required=False)
    link2 = forms.CharField(max_length=256, required=False)
    video_format = forms.CharField(max_length=120, required=False)
    unique_id = forms.CharField(max_length=120, required=False)


class LinkAjax(forms.Form):
    link = forms.CharField(max_length=256, required=False)
