from ecommapp import views
from django.urls import path
from ecommapp.views import ContactForm
from django.conf import settings
from django.conf.urls.static import static
'''
urlpatterns = [
    path('about',views.about),
    path('delete/<rid>',views.delete),
    path('contact/<rid>',ContactForm.as_view()),
    path('hello',views.hello),
    path('base',views.base),
    path('contact',views.contact),
]
'''
urlpatterns=[
    path('products',views.products),
    path('register',views.register),
    path('login',views.user_login),
    path('logout',views.user_logout),
    path('catfilter/<cv>',views.catfilter),
    path('sort/<sv>',views.sort),
    path('pricefilter',views.pricefilter),
    path('product_detail/<pid>',views.product_detail),
    path('addtocart/<pid>',views.cart),
    path('viewcart',views.viewcart),
    path('updateqty/<x>/<cid>',views.updateqty),
    path('removecart/<cid>',views.removecart),
    path('placeorder',views.placeorder),
    path('fetchorder',views.fetchorder),
    path('makepayment',views.makepayment),
    path('paymentsuccess',views.paymentsuccess),
    path('search',views.search),
]


if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)