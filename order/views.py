from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

from order.models import ShopCartForm, ShopCart
from product.models import Category

# Create your views here.

def index(request):
    return HttpResponse("Order App")

@login_required(login_url='/login')
def addtocart(request,id):
    url = request.META.get('HTTP_REFERER')
    current_user = request.user
    checkproduct = ShopCart.objects.filter(product_id=id)
    if checkproduct:
        control = 1
    else:
        control = 0

    if request.method == 'POST':
        form = ShopCartForm(request.POST)

        if form.is_valid(): #detailden tıklandıysa
            if control==1: #ürün varsa
                data = ShopCart.objects.get(product_id=id)
                data.quantity += form.cleaned_data['quantity']
                data.save()
            else: #ürün yoksa
                data= ShopCart()
                data.user_id = current_user.id
                data.product_id = id
                data.quantity = form.cleaned_data['quantity']
                data.save()
        request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
        messages.success(request, "Araç Başarılı Bir Şekilde Sepetinize Eklenmiştir..")
        return HttpResponseRedirect(url)
    else: #contentten tıklandıysa
        if control == 1:  # ürün varsa
            data = ShopCart.objects.get(product_id=id)
            data.quantity += 1
            data.save()
        else:  # ürün yoksa
            data = ShopCart()
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            data.save()
        request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
        messages.success(request, "Araç Başarılı Bir Şekilde Sepetinize Eklenmiştir..")
        return HttpResponseRedirect(url)

    messages.warning(request, "Sepete Eklemede Hata Oluştu..")
    return HttpResponseRedirect(url)






@login_required(login_url='/login')
def shopcart(request):
    category = Category.objects.all()
    current_user = request.user
    schopcart = ShopCart.objects.filter(user_id = current_user.id)
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
    total = 0
    for rs in schopcart:
        total += rs.product.price * rs.quantity

    context = {'schopcart': schopcart,
               'category' : category,
               'total' : total,
    }
    return render(request, 'Shopcart_products.html',context)

@login_required(login_url='/login')
def deletefromcart(request,id):
    ShopCart.objects.filter(id=id).delete()
    current_user = request.user
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
    messages.success(request,"Aracınız Sepetten Silindi.")
    return HttpResponseRedirect("/shopcart")