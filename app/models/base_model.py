from app.utils import db
from sqlalchemy import exc
from datetime import datetime
from app.utils import to_camel_case
from sqlalchemy.inspection import inspect
from app.repositories.base_repo import BaseRepo

class BaseModel(db.Model):
	__abstract__ = True
	
	id = db.Column(db.Integer(), primary_key=True)
	is_deleted = db.Column(db.Boolean, default=False, nullable=False)
	created_at = db.Column(db.DateTime(), default=datetime.now())
	updated_at = db.Column(db.DateTime(), default=datetime.now(), onupdate=datetime.now())
	
	def save(self):
		try:
			db.session.add(self)
			db.session.commit()
		except (exc.IntegrityError, exc.InvalidRequestError):
			db.session().rollback()
	
	def delete(self):
		db.session.delete(self)
		db.session.commit()
		
	def serialize(self):
		s = {to_camel_case(column.name): getattr(self, column.name) for column in self.__table__.columns if column.name not in ['created_at', 'updated_at']}
		s['timestamps'] = {'created_at': self.created_at, 'updated_at': self.updated_at, 'date_pretty_short': self.created_at.strftime('%b %d, %Y'),
						   'date_pretty': self.created_at.strftime('%B %d, %Y')}
		return s

