from app.controllers.base_controller import BaseController

class HomeController(BaseController):
	def __init__(self, request):
		BaseController.__init__(self, request)
		
	def home_page(self):
		return self.handle_response('OK', payload={'vessel': 'Welcome Message'})