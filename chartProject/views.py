from chartit import DataPool, Chart
from django.http import HttpResponse
from django.shortcuts import render, render_to_response

# Create your views here.
from chartProject.models import SalesReport, SalesHistory


def home(request):
    first_graph = "My First django_chartit graph"
    return HttpResponse(first_graph)


def monthName(month_nam):
    names = {1: 'JAM', 2: 'FEB', 3: 'MAR', 4: 'APR', 5: 'MAY', 6: 'JUNE', 7: 'JULY', 8: 'AUG', 9: 'SEP', 10: 'OCT',
             11: 'NOV', 12: 'DEC'}
    return names[month_nam]


def sales(request):
    sales = DataPool(
        series=
        [{'options': {
            # 'source': SalesReport.objects.all()},
            # 'source': SalesReport.objects.filter(sales__lte=20.00)},
            'source': SalesReport},
            'terms': [{'month': 'month', 'sales': 'sales'}]
        }

        ])

    # sales = DataPool(
    #     series=
    #     [{'options': {
    #         'source': SalesReport.objects.filter(sales_lte=20.00)},
    #         'terms': [{
    #                 'month': 'month',
    #                 'sales': 'sales'}]
    #
    #     ])

    cht = Chart(
        datasource=sales,
        series_options=
        [{'options': {
            'type': 'column',
            'stacking': False},
            'terms': {
                'month': [
                    'sales']
            }}],
        chart_options=
        {'title': {
            'text': 'Sales Amount Over Months'},
            'xAxis': {
                'title': {'text': 'Sales Total'}},
            'yAxis': {
                'title': {'text': 'Month Number'}}},
        x_sortf_mapf_mts=(None, monthName, False))

    cht2 = Chart(
        datasource=sales,
        series_options=
        [{'options': {
            'type': 'pie',
            'stacking': False},
            'terms': {
                'month': [
                    'sales']
            }}],
        chart_options=
        {'title': {
            'text': 'Sales Amount Over Months - Pie Chart'},
            'xAxis': {
                'title': {'text': 'Sales Total'}},
            'yAxis': {
                'title': {'text': 'Month Number'}}},
        x_sortf_mapf_mts=(None, monthName, False))

    return render(request, 'sales.html', {'chart_list': [cht, cht2]})


def citySales(request):
    ds = DataPool(
        series=[{
            'options': {
                'source': SalesHistory,
            },
            'terms': [
                'city',
                'sale_qty'
            ]
        }]
    )
    cht3 = Chart(
        datasource=ds,
        series_options=[{
            'options': {
                'type': 'bar',
                'stacking': True,
                'stack': 0,
            },
            'terms': {
                'city': [
                    'sale_qty'
                ]
            }},
        ],
        chart_options={
            'title': {
                'text': 'Sales reports'
            },
            'xAxis': {
                'title': {
                    'text': 'City'
                },
                'legend': {
                    "reversed": True,
                }

            }
        }
    )
    return render_to_response('citySales.html', {'citySales': cht3})
