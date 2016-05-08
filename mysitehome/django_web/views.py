from django.shortcuts import render
from django_web.models import ItemInfo
from django.core.paginator import Paginator


# Create your views here.
# 贴子列表#####################################################
def index(request):
    limit = 10
    item_info = ItemInfo.objects
    paginator = Paginator(item_info, limit)
    page = request.GET.get('page', 1)
    loaded = paginator.page(page)
    context = {
        'ItemInfo': loaded,
        'counts': item_info.count(),
        'last_time': item_info.order_by('-pub_date').limit(1)
    }
    return render(request, 'index_data.html', context)


##############################################################

# 发贴量TOP3#####################################################
def topx(date1, date2, area, limit):
    options = {
        'chart': {'zoomType': 'xy'},
        'title': {'text': '发贴数量最大的类目'},
        'subtitle': {'text': '数据图表'},
        'yAxis': {'title': {'text': '数量'}}
    }
    pipeline = [
        {'$match': {'$and': [{'pub_date': {'$gte': date1, '$lte': date2}}, {'area': {'$all': area}}]}},
        {'$group': {'_id': {'$slice': ['$cates', 2, 1]}, 'counts': {'$sum': 1}}},
        {'$limit': limit},
        {'$sort': {'counts': -1}}
    ]

    for i in ItemInfo._get_collection().aggregate(pipeline):
        data = {
            'name': i['_id'][0],
            'data': [i['counts']],
            'type': 'column'
        }
        yield data


series_CY = [i for i in topx('2015.12.25', '2016.03.25', ['朝阳'], 3)]
series_HD = [i for i in topx('2015.12.25', '2016.03.25', ['海淀'], 3)]
series_TZ = [i for i in topx('2015.12.25', '2016.03.25', ['通州'], 3)]


################################################################

# 发帖总量柱状图##################################################
def total_post():
    pipeline = [
        {'$group': {'_id': {'$slice': ['$cates', 2, 1]}, 'counts': {'$sum': 1}}},
    ]

    for i in ItemInfo._get_collection().aggregate(pipeline):
        data = {
            'name': i['_id'][0],
            'y': i['counts']
        }
        yield data


series_post = [i for i in total_post()]


#################################################################

# 饼图############################################################
def one_day_deal_cate():
    pipeline = [
        {'$match': {'$and': [{'pub_date': {'$gte': '2015.12.25', '$lte': '2016.03.25'}}, {'time': 1}]}},
        {'$group': {'_id': {'$slice': ['$cates', 2, 1]}, 'counts': {'$sum': 1}}},
        {'$sort': {'counts': 1}}
    ]

    for i in ItemInfo._get_collection().aggregate(pipeline):
        data = {
            'name': i['_id'][0],
            'y': i['counts']
        }
        print(data)
        yield data


def one_day_deal_area():
    pipeline = [
        {'$match': {'$and': [{'pub_date': {'$gte': '2015.12.25', '$lte': '2016.03.25'}}, {'time': 1}]}},
        {'$group': {'_id': {'$slice': ['$area', 1]}, 'counts': {'$sum': 1}}},
        {'$sort': {'counts': 1}}
    ]

    for i in ItemInfo._get_collection().aggregate(pipeline):
        data = {
            'name': i['_id'][0],
            'y': i['counts']
        }
        yield data


pie1_data = [i for i in one_day_deal_cate()]
pie2_data = [i for i in one_day_deal_area()]


###############################################################


def chart(request):
    context = {
        'chart_CY': series_CY,
        'chart_HD': series_HD,
        'chart_TZ': series_TZ,
        'series_post': series_post,
        'pie1_data': pie1_data,
        'pie2_data': pie2_data
    }
    return render(request, 'chart1.html', context)

