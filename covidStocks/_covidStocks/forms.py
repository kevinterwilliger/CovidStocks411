from django import forms
from .models import Tweets,Company
class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweets
        exclude = ('tweetID','companyID','date')
class TweetEdit(forms.Form):
    tweetID = forms.IntegerField(required=True)
    companyID = forms.ModelChoiceField(required=False, queryset=Company.objects.values('companyID'))
    date = forms.DateField(required=False,input_formats=['%b. %d, %Y'])
    text = forms.CharField(max_length=280)
    userID = forms.CharField(max_length=None)
    score = forms.FloatField()
    interactions = forms.IntegerField()
