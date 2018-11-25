from app.utils import db
from sqlalchemy import exc
from datetime import datetime
from sqlalchemy.inspection import inspect
from app.repositories.base_repo import BaseRepo
from app.utils import to_camel_case, format_response_timestamp


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
		s['timestamps'] = {'createdAt': format_response_timestamp(self.created_at), 'updatedAt': format_response_timestamp(self.updated_at)}
		return s

