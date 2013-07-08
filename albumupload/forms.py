from django import forms

class UploadFileForm(forms.Form):
    album_name = forms.CharField(max_length=150)
    myfiles = forms.FileField()
