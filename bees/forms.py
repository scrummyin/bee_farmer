from django import forms


class CreateNodeForm(forms.Form):
    path = forms.CharField(widget=forms.HiddenInput, required=True)
    node_name = forms.CharField()
    value = forms.CharField(required=False)

class EditNodeForm(forms.Form):
    path = forms.CharField(widget=forms.HiddenInput, required=True)
    value = forms.CharField()
