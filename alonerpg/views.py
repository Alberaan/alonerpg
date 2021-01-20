from .tablesreader import *
from django.views.generic.base import TemplateView

class HomePageView(TemplateView):

    template_name = "home.html"

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        #context['parametros'] = request.GET["ls"]
        command = request.GET["command"]
        tables = get_tables()
        result = dynamic_call(tables, command)
        context["message"] = result.message
        context["data"] = get_text(result.data)

        return self.render_to_response(context)

def get_text(data):
    text = []
    if isinstance(data, str):
        text.append(data)
    if isinstance(data, list):
        for table in data:
            if isinstance(table, Table):
                text.append(str(table.index) + ": (" + table.system + ") " + table.filename)
    return text
    
