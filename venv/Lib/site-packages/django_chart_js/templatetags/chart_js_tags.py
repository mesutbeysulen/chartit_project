from random import choice, randint
from string import ascii_letters, digits

from django import template
from django.template.base import Node
from django.utils.html import format_html
from django.utils.safestring import mark_safe

# from django.contrib.staticfiles.storage import staticfiles_storage
import json

LETTERS_AND_DIGITS = ascii_letters + digits

register = template.Library()


@register.tag
def chartjs(parser, token):
    return ChartJs(parser, token)


class ChartJs(Node):
    """
    Using:
    {% chartjs 400x300 data line %}  You should pull data in context
    Chart types are: line, bar, radar
    Data formats:
    Short:
    > data = [x**2 for x in range(20)]
    or
    > data = [x*2 for x in range(15)], [2/x for x in range(16)]
    or full:
    > data = {
    >     'labels': ['Jan', 'May', 'Nov', 'Dec'],
    >     'datasets': [
    >         {
    >             'label': 'My very own chart',
    >             'data': [50, 40, -40, 800],
    >             'fillColor': 'rgba(220, 220, 220, 0.2)',
    >         },
    >         {
    >             'data': [10, 20, 30, 40],
    >             'pointColor': '#fefedf',
    >         }
    >      ]
    > }
    See all options in Chart.js docs: http://www.chartjs.org/docs/
    If you don't choose color it will be generated randomly.
    """
    CHART_PARAMETERS = ('fillColor', 'strokeColor', 'pointColor', 'pointHighlightStroke')
    DEFAULT_OPACITY = 0.8

    def __init__(self, parser, token):
        self.parser = parser
        self.token = token.split_contents()

    def render(self, context):
        # TODO: Use local staticfiles instead of CDN's. May be specify behavior in settings?
        assert len(self.token) == 4, 'Make sure you\'ve specified size, data and type for the chart.'
        chart_type = self.token[3].title()
        assert chart_type in ('Line', 'Bar', 'Radar'), \
            'Only Line, Bar and Radar chars are supported. You type is: %s' % chart_type
        size = list(map(int, self.token[1].split('x')))
        canvas_data = self.fill_data(template.Variable(self.token[2]).resolve(context))
        # TODO: Use something better than generate random seq.
        canvas_id = ''.join(choice(LETTERS_AND_DIGITS) for _ in range(3))
        js_canvas_data = mark_safe(json.dumps(canvas_data, ensure_ascii=False))
        data = {
            'canvas_id': canvas_id,
            'chart_type': chart_type,
            'canvas_data': js_canvas_data,
            'canvas_width': size[0],
            'canvas_height': size[1],
            'options': '',
            'jquery_lib': 'https://code.jquery.com/jquery-2.1.4.min.js',  # staticfiles_storage.url('css/Chart.min.js')
            'chart_js_lib': 'https://cdnjs.cloudflare.com/ajax/libs/Chart.js/1.0.2/Chart.min.js',
        }
        # TODO: Make away with jQuery. It requires only to parse JSON.
        return format_html('''
            <script type="text/javascript" src="{jquery_lib}"></script>
            <script type="text/javascript" src="{chart_js_lib}"></script>
            <canvas id="chart_{canvas_id}" width="{canvas_width}" height="{canvas_height}"></canvas>
            <script type="text/javascript">
                var chart_{canvas_id}_data = jQuery.parseJSON('{canvas_data}');
                var context_{canvas_id} = document.getElementById("chart_{canvas_id}").getContext("2d");
                var chart_{canvas_id} = new Chart(context_{canvas_id}).{chart_type}(chart_{canvas_id}_data);
            </script>
            ''', **data)

    def fill_data(self, variable):
        if 'generator' in str(variable.__class__):
            variable = tuple(variable)
        if isinstance(variable, (tuple, list)):
            # now determine, is it list of lists or list of values
            if isinstance(variable[0], (tuple, list)):
                charts = [chart[:] for chart in variable]
                del variable
                variable = {'datasets': [{'data': data} for data in charts]}
            else:
                data = variable[:]
                del variable
                variable = {'datasets': [{'data': data}]}
        assert 'datasets' in variable, 'At least one data set must be in.'
        if 'labels' not in variable:
            max_length = max([len(set_['data']) for set_ in variable['datasets']])
            variable['labels'] = ['' for _ in range(max_length)]
        for set_ in variable['datasets']:
            random_color = 'rgba({r}, {g}, {b}, {opacity})'.format(r=randint(0, 220), g=randint(0, 220),
                                                                   b=randint(0, 220), opacity=self.DEFAULT_OPACITY)
            for param in self.CHART_PARAMETERS:
                set_.setdefault(param, random_color)
        return variable
