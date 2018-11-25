
class BaseRepo:
	
	def __init__(self, _model):
		self._model = _model
		
	def fetch_all(self):
		"""Return all the data in the model."""
		return self._model.query.paginate(error_out=False)
	
	def get(self, *args):
		"""Return data by the Id."""
		return self._model.query.get(*args)
	
	def update(self, model_instance, **kwargs):
		""" Update Model """
		for key, val in kwargs.items():
			setattr(model_instance, key, val)
		model_instance.save()
		return model_instance
	
	def count(self):
		"""Return the count of all the data in the model."""
		return self._model.query.count()
	
	def get_first_item(self):
		"""Return the first data in the model."""
		return self._model.query.first()
	
	def order_by(self, *args):
		"""Query and order the data of the model."""
		return self._model.query.order_by(*args)
	
	def filter_all(self, **kwargs):
		"""Query and filter the data of the model."""
		return self._model.query.filter(**kwargs).paginate(error_out=False)
	
	def filter_by(self, **kwargs):
		"""Query and filter the data of the model."""
		return self._model.query.filter_by(**kwargs).paginate(error_out=False)
	
	def find_first(self, **kwargs):
		"""Query and filter the data of a model, returning the first result."""
		return self._model.query.filter_by(**kwargs).first()
	
	def filter_and_count(self, **kwargs):
		"""Query, filter and counts all the data of a model."""
		return self._model.query.filter_by(**kwargs).count()
	
	def filter_and_order(self, *args, **kwargs):
		"""Query, filter and orders all the data of a model."""
		return self._model.query.filter_by(**kwargs).order_by(*args)
	
	def paginate(self, **kwargs):
		"""Query and paginate the data of a model, returning the first result."""
		return self._model.query.paginate(**kwargs)
	
	def filter(self, *args):
		"""Query and filter the data of the model."""
		return self._model.query.filter(*args)
	
	def pagination_meta(self, paginator):
		return {'totalRows': paginator.total, 'totalPages': paginator.pages, 'currentPage': paginator.page,
				'nextPage': paginator.next_num, 'prevPage': paginator.prev_num}
