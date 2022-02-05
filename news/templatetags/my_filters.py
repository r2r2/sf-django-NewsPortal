from string import punctuation

from django import template

from NewsPortal.settings import BAD_WORDS

register = template.Library()
punctuation = punctuation + '...'


@register.filter(name='censor')
def censor(value: str):
    with open(BAD_WORDS, 'r', encoding='utf-8') as f:
        mat = f.read().split(', ')
        value = value.split()
        i = 0
        while i < len(value):
            if value[i].strip(punctuation).lower() in mat and value[i] not in punctuation:
                value[i] = '✗' * len(value[i])
                i = 0
            i += 1
        value = ' '.join(value)
        return value



