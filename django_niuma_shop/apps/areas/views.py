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
            provinces = Area.objects.filter(parent_id = None)
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

class SubAreaView(View):

    def get(self, request, id):

        # 先进行获取缓存数据
        data_list = cache.get('city:%s'%id)

        if not data_list:
            # 1. 获取省份id 市的id 查询信息
            up_level = Area.objects.filter(id = id).first()
            down_level = up_level.subs.all()
            # 2. 将对象数据转换为字典数据
            data_list = []
            for item in down_level:
                data_list.append({
                    'id': item.id,
                    'name': item.name
                })
            cache.set('city:%s'%id, data_list, 24*3600)
        return JsonResponse({ 'code': 0, 'errmsg': 'ok', 'sub_data': {'subs': data_list} })