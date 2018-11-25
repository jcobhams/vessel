from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


def to_camel_case(snake_str):
	"""Format string to camel case."""
	title_str = snake_str.title().replace("_", "")
	return title_str[0].lower() + title_str[1:]


def to_pascal_case(word, sep='_'):
	return ''.join(list(map(lambda x: x.capitalize(), word.split(sep))))


def format_response_timestamp(date_obj):
	if isinstance(date_obj, datetime):
		return {'isoDate': date_obj.isoformat(), 'datePretty': date_obj,
				'datePrettyShort': date_obj.strftime('%b %d, %Y')}