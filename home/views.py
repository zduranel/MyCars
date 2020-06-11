import json

from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from content.models import Content, Menu, CImages
from home.forms import SearchForm, SignUpForm
from home.models import Setting, ContactFormu, ContactFormMessage, UserProfile
from order.models import ShopCart
from product.models import Product, Category, Images, Comment



def index(request):
    current_user = request.user
    setting = Setting.objects.get(pk=1)
    sliderdata = Product.objects.all()[:4]
    category = Category.objects.all()
    menu = Menu.objects.all()
    dayproducts = Product.objects.all()[:4]
    lastproducts = Product.objects.all().order_by('-id')[:4]
    randomproducts = Product.objects.all().order_by('?')[:4]
    request.session['cart_items'] = ShopCart.objects.filter(user_id=current_user.id).count()
    news = Content.objects.filter(type='haber').order_by('-id')[:4]
    announcements = Content.objects.filter(type='duyuru').order_by('-id')[:4]

    profile = UserProfile.objects.get(user_id=current_user.id)


    context = {'setting': setting, 'page':'home',
                'category': category,
                'menu': menu,
                'news': news,
                'announcements': announcements,
                'sliderdata' : sliderdata,
                'dayproducts' : dayproducts,
                'lastproducts' : lastproducts,
                'randomproducts' : randomproducts,
                'profile': profile


               }
    return render(request, 'index.html', context)


def hakkimizda(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting, 'page': 'hakkimizda'}
    return render(request, 'hakkimizda.html', context)


def referanslar(request):
    setting = Setting.objects.get(pk=1)
    context = {'setting': setting, 'page': 'referanslar'}
    return render(request, 'referanslar.html', context)


def iletisim(request):

    if request.method == 'POST':
        form = ContactFormu(request.POST)
        if form.is_valid():
            data = ContactFormMessage()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.subject = form.cleaned_data['subject']
            data.message = form.cleaned_data['message']
            data.ip = request.META.get('REMOTE_ADDR')
            data.save()
            messages.success(request, "Mesaj Gönderildi! Teşekkürler")
            return HttpResponseRedirect ('/iletisim')


    setting = Setting.objects.get(pk=1)
    form= ContactFormu()
    context = {'setting': setting,'form': form}
    return render(request, 'iletisim.html', context)


def categoryproducts(request, id, slug):
    category = Category.objects.all()
    categorydata = Category.objects.get(pk=id)
    products = Product.objects.filter(category_id=id)
    context = {'products': products,
               'category': category,
               'categorydata':categorydata

               }
    return render(request, 'products.html', context)

def product_details(request,id,slug):
    category = Category.objects.all()
    try:
        product = Product.objects.get(pk=id)
        images = Images.objects.filter(product_id=id)
        comments = Comment.objects.filter(product_id=id,status ='True')
        context = {'product': product,
                   'category': category,
                   'images': images,
                   'comments' : comments

                   }
        return render(request, 'product_detail.html',context)

    except:
        messages.warning(request, "Hata! İlgili İçerik Bulunamadı")
        link = '/error'
        return HttpResponseRedirect(link)


def product_search(request):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            category = Category.objects.all()
            query = form.cleaned_data['query']
            products = Product.objects.filter(title__icontains=query)
           # else:
           #       products = Product.objects.filter(title__icontains=query,category_id=catid)

            context = {'products': products,
                       'category': category

                      }

            return render(request, 'products_search.html', context)
    return HttpResponseRedirect('/')

def product_asearch(request):
    return render(request, 'asearch.html')

def product_search_auto(request):
    if request.is_ajax():
        q = request.GET.get('term', '')
        product = Product.objects.filter(title__icontains=q)
        results = []
        for rs in product:
            product_json = {}
            product_json = rs.title
            results.append(product_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data,mimetype)

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            messages.warning(request, "Kullanıcı adı veya şifre hatalı")
            return HttpResponseRedirect('/login')


    category = Category.objects.all()
    context =       {'category': category,

                    }

    return render(request, 'login.html', context)


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate( username=username, password=password)
            login(request, user)
            current_user = request.user
            data = UserProfile()
            data.user_id = current_user.id
            data.image = "images/users/user.png"
            data.save()
            messages.success(request,"ÜYE BAŞARILI")
            return HttpResponseRedirect('/')


    form = SignUpForm()
    category = Category.objects.all()
    context = {'category': category,
               'form' : form,
              }

    return render(request, 'signup.html', context)

def menu(request, id):
    try:
        content = Content.objects.get(menu_id=id)
        link = '/content/' + str(content.id) + '/menu'
        return HttpResponseRedirect(link)
    except:
        messages.warning(request, "Hata! İlgili İçerik Bulunamadı")
        link = '/error'
        return HttpResponseRedirect(link)

def contentdetail(request,id,slug):
    category = Category.objects.all()
    menu = Menu.objects.all()
    try:
        content = Content.objects.get(pk=id)
        images = CImages.objects.filter(content_id=id)

        context = {'content': content,
                   'category': category,
                   'menu': menu,
                   'images': images,
                   }

        return render(request, 'content_detail.html',context)

    except:
        messages.warning(request, "Hata! İlgili İçerik Bulunamadı")
        link = '/error'
        return HttpResponseRedirect(link)

def error(request):
    category = Category.objects.all()
    menu = Menu.objects.all()


    context = {'category': category,
               'menu': menu,
               }

    return render(request, 'error_page.html', context)





