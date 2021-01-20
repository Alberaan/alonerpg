from .tablesreader import *
from django.views.generic.base import TemplateView

class HomePageView(TemplateView):

    template_name = "home.html"
    tables = get_tables()

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        if "command" in request.GET:
            command = request.GET["command"]
        if "searchfield" in request.GET:
            command = "lt " + request.GET["searchfield"]

        result = dynamic_call(self.tables, command)
        context["message"] = result.message
        context["result"] = ""
        context["tables"] = ""

        if isinstance(result.data, str):
            context["result"] = result.data
        if isinstance(result.data, list):
            context["tables"] = result.data

        return self.render_to_response(context)
