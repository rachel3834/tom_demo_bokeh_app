from guardian.mixins import PermissionListMixin
from django_filters.views import FilterView
from tom_targets.models import Target
import json
from django.shortcuts import render
from django.http import HttpResponse
from bokeh.plotting import figure
from bokeh.embed import components


class TableView(FilterView):
    """
    View for listing targets in the TOM. Only shows targets that the user is authorized to view. Requires authorization.
    """
    template_name = 'table_list.html'
    paginate_by = 25
    strict = False
    model = Target
    permission_required = 'tom_targets.view_target'
    ordering = ['-created']

    def get_context_data(self, *args, **kwargs):
        """
        Adds the number of targets visible, the available ``TargetList`` objects if the user is authenticated, and
        the query string to the context object.

        :returns: context dictionary
        :rtype: dict
        """
        context = super().get_context_data(*args, **kwargs)
        
        script, div = self._bokeh_data_table()
        context['bokeh_script'] = script
        context['bokeh_div'] = div

        return context

    def _bokeh_plot(self):
        # create a plot
        plot = figure(width=400, height=400)

        # add a circle renderer with a size, color, and alpha

        plot.circle([1, 2, 3, 4, 5], [6, 7, 2, 4, 5], size=20, color="navy", alpha=0.5)

        script, div = components(plot)

        return script, div

    def _bokeh_data_table(self):
        from bokeh.layouts import column
        from bokeh.models import (ColumnDataSource, DataTable, HoverTool, IntEditor,
                                  NumberEditor, NumberFormatter, SelectEditor,
                                  StringEditor, StringFormatter, TableColumn)
        from bokeh.plotting import figure, show
        from bokeh.sampledata.autompg2 import autompg2 as mpg

        source = ColumnDataSource(mpg)

        manufacturers = sorted(mpg["manufacturer"].unique())
        models = sorted(mpg["model"].unique())
        transmissions = sorted(mpg["trans"].unique())
        drives = sorted(mpg["drv"].unique())
        classes = sorted(mpg["class"].unique())

        columns = [
            TableColumn(field="manufacturer", title="Manufacturer",
                        editor=SelectEditor(options=manufacturers),
                        formatter=StringFormatter(font_style="bold")),
            TableColumn(field="model", title="Model",
                        editor=StringEditor(completions=models)),
            TableColumn(field="displ", title="Displacement",
                        editor=NumberEditor(step=0.1), formatter=NumberFormatter(format="0.0")),
            TableColumn(field="year", title="Year", editor=IntEditor()),
            TableColumn(field="cyl", title="Cylinders", editor=IntEditor()),
            TableColumn(field="trans", title="Transmission",
                        editor=SelectEditor(options=transmissions)),
            TableColumn(field="drv", title="Drive", editor=SelectEditor(options=drives)),
            TableColumn(field="class", title="Class", editor=SelectEditor(options=classes)),
            TableColumn(field="cty", title="City MPG", editor=IntEditor()),
            TableColumn(field="hwy", title="Highway MPG", editor=IntEditor()),
        ]
        data_table = DataTable(source=source, columns=columns, editable=True, width=800,
                               index_position=-1, index_header="row index", index_width=60)

        p = figure(width=800, height=300, tools="pan,wheel_zoom,xbox_select,reset", active_drag="xbox_select")

        cty = p.scatter(x="index", y="cty", fill_color="#396285", size=8, alpha=0.5, source=source)
        hwy = p.scatter(x="index", y="hwy", fill_color="#CE603D", size=8, alpha=0.5, source=source)

        tooltips = [
            ("Manufacturer", "@manufacturer"),
            ("Model", "@model"),
            ("Displacement", "@displ"),
            ("Year", "@year"),
            ("Cylinders", "@cyl"),
            ("Transmission", "@trans"),
            ("Drive", "@drv"),
            ("Class", "@class"),
        ]
        cty_hover_tool = HoverTool(renderers=[cty], tooltips=[*tooltips, ("City MPG", "@cty")])
        hwy_hover_tool = HoverTool(renderers=[hwy], tooltips=[*tooltips, ("Highway MPG", "@hwy")])

        p.add_tools(cty_hover_tool, hwy_hover_tool)

        scripts, divs = components((p, data_table))

        return scripts, divs