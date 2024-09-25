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

@register.filter
def hide_forbidden(value):
	words = value.split()
	result = []
	for word in words:
		if word in BAD_WORDS:
			result.append(word[0] + "*"*(len(word)-2) + word[-1])
        else:
		result.append(word)
	return " ".join(result)