from django import forms
from .models import File

class EmailForm(forms.Form):
    email = forms.EmailField()
    file = forms.ModelChoiceField(queryset=File.objects.none())  # Start with an empty queryset

    def __init__(self, *args, **kwargs):
        file_instance = kwargs.pop('file_instance', None)
        super(EmailForm, self).__init__(*args, **kwargs)
        if file_instance:
            # Set the queryset to only include the specific file instance
            self.fields['file'].queryset = File.objects.filter(pk=file_instance.pk)



class FileUploadForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['title', 'description', 'file']