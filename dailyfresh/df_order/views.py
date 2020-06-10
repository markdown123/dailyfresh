from django.shortcuts import render
from df_user.models import UserInfo


def order(request):
    """
     此函数用户给下订单页面展示数据
    接收购物车页面GET方法发过来的购物车中物品的id，构造购物车对象供订单使用
    """
    uid = request.session.get('user_id')
    user = UserInfo.objects.get(id=uid)
    return render(request,'df_order/place_order.html')

def order_handle(request):
    """
    1 创建订单对象
    2 判断商品的库存
    3 创建详细订单对象
    4 修改商品库存
    5 删除购物车
    :param request:
    :return:
    """

