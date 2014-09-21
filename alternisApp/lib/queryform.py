from django import forms

class QueryForm(forms.Form):

    def set_initial(self):
        q = forms.CharField(
            widget=forms.TextInput(attrs={'class': 'form-control'}),
            max_length=200,
            initial=self,
            label=""
        )
        return q

    q = forms.CharField(
            widget=forms.TextInput(attrs={'class': 'form-control'}),
            max_length=200,
            initial='looking for some competition?',
            label=""
        )