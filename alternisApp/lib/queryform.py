from django import forms

class QueryForm(forms.Form):
    q = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        max_length=200,
        initial='looking for some competition?',
        label=""
        )