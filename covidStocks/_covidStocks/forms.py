from django import forms
from .models import Tweets,Company
class TweetForm(forms.ModelForm):
    class Meta:
        model = Tweets
        fields = "__all__"
class TweetEdit(forms.Form):
    tweetID = forms.IntegerField(required=True)
    companyID = forms.ModelChoiceField(queryset=Company.objects.values('companyID'))
    date = forms.DateTimeField()
    text = forms.CharField(max_length=280)
    userID = forms.CharField(max_length=None)
    score = forms.FloatField()
    interactions = forms.IntegerField()
