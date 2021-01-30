from .settings import TABLES_PATH
from .tablesreader import *
from django.views.generic.base import TemplateView


class HomePageView(TemplateView):

    template_name = "home.html"
    tables = get_tables(TABLES_PATH)

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        rolled_table = ""

        if "rtn" in request.GET:
            command = "rtn " + request.GET["rtn"]
            roll_result = dynamic_call(self.tables, command)
            if isinstance(roll_result.data, str):
                context["roll_data"] = roll_result.data
                context["roll_message"] = roll_result.message
                rolled_table = int(request.GET["rtn"])
            
        if "searchfield" in request.GET:
            command = "lt " + request.GET["searchfield"]
            filtered_tables = dynamic_call(self.tables, command)
            if isinstance(filtered_tables.data, list):
                context["tables"] = filtered_tables.data
                context["filter_message"] = filtered_tables.message
                context["current_filter"] = request.GET["searchfield"]
                context["rolled_table"] = rolled_table

        if len(request.GET) == 0:
            filtered_tables = dynamic_call(self.tables, "lt")
            if isinstance(filtered_tables.data, list):
                context["tables"] = filtered_tables.data
                context["filter_message"] = filtered_tables.message
                context["current_filter"] = ""

        return self.render_to_response(context)
