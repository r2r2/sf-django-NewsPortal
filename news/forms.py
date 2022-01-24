from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django.forms import ModelForm, Textarea, ModelMultipleChoiceField, TextInput, ChoiceField
from django import forms
from .models import Post, Category


class PostForm(ModelForm):
    """Форма добавления статьи на сайт"""

    category = ModelMultipleChoiceField(queryset=Category.objects.all(), label='Категория', to_field_name='category_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields['category'].empty_label = "Категория не выбрана"
        self.fields['author'].empty_label = "Автор не выбран"

    class Meta:
        model = Post
        fields = ['post_title', 'post_text', 'category', 'author']
        widgets = {
            'post_title': TextInput(attrs={'class': 'form-input'}),
            'post_text': Textarea(attrs={'cols': 60, 'rows': 10, 'class': 'form-input'}),
            # 'category': ChoiceField(attrs={'class': 'form-input'})
        }


class CommonSignupForm(SignupForm):
    """Автоматическое добавление зарегистрированного пользователя в общую группу"""
    def save(self, request):
        user = super(CommonSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user


# Если регистрируется через Гугл # TODO make self adding to "common" group through Google
# class LocalSignupForm(forms.Form):
#     pass
#
#     def signup(self, request, user):
#         group = Group.objects.get(name="common")
#         user.groups.add(group)
#         user.save()

































