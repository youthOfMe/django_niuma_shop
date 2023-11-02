from django.core.cache import cache
from django.shortcuts import render
from django.views import View

# Create your views here.
from apps.areas.models import Area
from django.http import JsonResponse
class AreaView(View):

    def get(self, request):

        # 先进行去查询缓存中的数据
        province_list = cache.get('province')
        # 如果没有缓存就去数据库进行查询数据
        if not province_list:
            provinces = Area.objects.filter()
            province_list = []
            for province in provinces:
                province_list.append({
                    'id': province.id,
                    'name': province.name
                })
            # 保存缓存数据
            cache.set('province', province_list, 24 * 3600)
        # 返回响应
        return JsonResponse({ 'code': 0, 'errmsg': 'ok', 'province_list': province_list })