from django import forms 
from .models import MyWish, Comment

class TodoForm(forms.Form):
    text = forms.CharField(max_length=40, 
        widget=forms.TextInput(
            attrs={'class' : 'form-control', 'placeholder' : '오늘의 할 일 목록을 적어주세요!', 'aria-label' : 'Todo', 'aria-describedby' : 'add-btn'}))
    

class MyWishForm(forms.ModelForm):
    class Meta:
        model = MyWish
        fields = ['checked_wish']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)