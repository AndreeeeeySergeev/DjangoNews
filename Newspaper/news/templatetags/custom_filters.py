from django import template

register = template.Library()

BAD_WORDS = [
	'bad_word_1',
	'bad_word_2',
	'bad_word_3',
]


@register.filter()
def censor(text):
	for i in BAD_WORDS:
		text = text.replace(i, '****')
		return text
