from django.db.models import query
from django.http import HttpResponse, response
from django.shortcuts import render
from django.template.defaultfilters import lower
from .models import Contact, Order, OrderUpdate, Product
from math import ceil, e
import json
from django.views.decorators.csrf import csrf_exempt
from Paytm import Checksum
# Create your views here.
MERCHANT_KEY = 'uub2#PFaDasr17WI'


def searchMatch(query, item):
    findplaces = [item.product_name, item.category,
                  item.subcategory, item.price, item.desc]
    findplaces = [lower(str(item)) for item in findplaces]
    for item in findplaces:
        if query in item:
            return True
    else:
        return False

def search(request):
    query = request.GET.get('search', '')
    catProds = Product.objects.values('category')
    cats = {item['category'] for item in catProds}
    allProds = []
    print(query)
    print("SXXXXXXXXXXXXXXXXXXXXXXXX")
    for cat in sorted(cats):
        prodtemp = Product.objects.filter(category=cat)
        prod = [item for item in prodtemp if searchMatch(query, item)]
        n = len(prod)
        if(n == 0):
            continue
        nslides = ceil(n/4)
        allProds.append([prod, range(1, nslides), n])
    if(len(allProds) == 0):
        return render(request, 'shop/search.html', {'allProds':allProds, 'msg' : True, 'query':query})
    return render(request, 'shop/search.html', {'allProds': allProds, 'msg' : False, 'query' : query})

def index(request):
    catProds = Product.objects.values('category')
    cats = {item['category'] for item in catProds}

    allProds = []
    for cat in sorted(cats):
        prod = Product.objects.filter(category=cat)
        n = len(prod)
        nslides = ceil(n/4)
        allProds.append([prod, range(1, nslides), n])
    return render(request, 'shop/index.html', {'allProds': allProds})




def about(request):
    return render(request, 'shop/about.html')


def contact(request):
    thanks = False
    if(request.method == 'POST'):
        name = request.POST.get('name', '')
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')
        query = request.POST.get('query', '')
        contact = Contact(name=name, phone=phone, email=email, query=query)
        contact.save()

    return render(request, 'shop/contact.html', {'thanks': thanks})


def tracker(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            order = Order.objects.filter(id=orderId, email=email)
            if len(order) > 0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append(
                        {'text': item.update_desc, 'time': item.timestamp})
                response = json.dumps(
                    [updates, order[0].items_json], default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse("e")

    return render(request, 'shop/tracker.html')


def products(request, id):
    product = Product.objects.filter(id=id)
    return render(request, 'shop/products.html', {'product': product[0]})


def checkout(request):
    if(request.method == 'POST'):
        name = request.POST.get('name', '')
        items_json = request.POST.get('items_json', 'error')
        amount = request.POST.get('amount', 0)
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        address = f"{request.POST.get('address1')}, {request.POST.get('address2', '')}"
        zip_code = request.POST.get('zip_code', '')

        order = Order(items_json=items_json, amount=amount, name=name, email=email, address=address,
                      city=city, state=state, zip_code=zip_code, phone=phone)
        order.save()
        update = OrderUpdate(
            order_id=order.id, update_desc="The Order has been placed")
        update.save()
        #  render(request, 'shop/checkout.html', {})
        # Request paytm to transfer the amount to your account after payment by user
        param_dict = {

            'MID': 'sDDbTZ57568196542685',
            'ORDER_ID': f"{order.id}",
            'TXN_AMOUNT': f"{amount}",
            'CUST_ID': email,
            'INDUSTRY_TYPE_ID': 'Retail',
            'WEBSITE': 'WEBSTAGING',
            'CHANNEL_ID': 'WEB',
            'CALLBACK_URL': 'http://127.0.0.1:8000/shop/handlerequest/',
        }
        print(order.id)
        print("XXXXXXXXXXXXXXXXXXxx")
        param_dict['CHECKSUMHASH'] = Checksum.generate_checksum(
            param_dict, MERCHANT_KEY)
        return render(request, 'shop/paytm.html', {'param_dict': param_dict, 'thanks': True, 'id': order.id})

    return render(request, 'shop/checkout.html', {'thanks': False})


@csrf_exempt
def handlerequest(request):
    # paytm will send you request here
    form = request.POST
    response_dict = {}
    for i in form.keys():
        response_dict[i] = form[i]
        if i == "CHECKSUMHASH":
            checksum = form[i]
    verify = Checksum.verify_checksum(response_dict, MERCHANT_KEY, checksum)
    if verify:
        if response_dict['RESPCODE'] == '01':
            print('order successful')
        else:
            print('order was not successful because', response_dict['RESPMSG'])

    return render(request, 'shop/paymentstatus.html', {'response': response_dict})


"""
    from django.utils import timezone
    handle = open("D:\Backend\mac\shop\static\shop\extract.html")
    link - photo - price - rating - name
    used for parsing the code
    for text in handle:
    text = text.strip()
    text = text.split("||||")
    link = text[0]
    photo = "shop/images/"+text[1]
    print(photo)
    price = int(text[2].replace(',', '').replace('.00', ''))
    print(price)
    rating = float(text[3])
    print(rating)
    product_name = text[4]
    print(product_name)
    print('description')
    category, subcategory = input().split()
    myprod = Product(product_name = product_name, category = category, subcategory = subcategory, price = price, desc = f"{rating} out of 5⭐", pub_date = timezone.now(), image = photo)
    myprod.save()
"""
