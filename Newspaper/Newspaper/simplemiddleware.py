class SimpleMiddleware:
	def __int__(self):
		self.get_response = get_response

	def __call__(self, request):
		response = self.get_response(request)
		if request.mobile:
			prefix = "mobile/"
		else:
			prefix = "full/"

		response.template_name = prefix + response.template_name

		return response
