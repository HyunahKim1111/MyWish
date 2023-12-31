from django import forms 

class TodoForm(forms.Form):
    text = forms.CharField(max_length=40, 
        widget=forms.TextInput(
            attrs={'class' : 'form-control', 'placeholder' : '오늘의 할 일 목록을 적어주세요!', 'aria-label' : 'Todo', 'aria-describedby' : 'add-btn'}))