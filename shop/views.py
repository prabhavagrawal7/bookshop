from django.http import HttpResponse
from django.shortcuts import render
from .models import Contact, Order, OrderUpdate, Product
from math import ceil
import json
# Create your views here.


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
    if(request.method == 'POST'):
        name = request.POST.get('name', '')
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')
        query = request.POST.get('query', '')
        contact = Contact(name=name, phone=phone, email=email, query=query)
        contact.save()

    return render(request, 'shop/contact.html')


def tracker(request):
    if request.method == "POST":
        orderId = request.POST.get('orderId', '')
        email = request.POST.get('email', '')
        try:
            orders = Order.objects.filter(id=orderId, email=email)
            if len(orders) > 0:
                update = OrderUpdate.objects.filter(order_id=orderId)
                updates = []
                for item in update:
                    updates.append({'text': item.update_desc, 'time': item.timestamp})
                    response = json.dumps(updates, default=str)
                return HttpResponse(response)
            else:
                return HttpResponse('{}')
        except Exception as e:
            return HttpResponse('{}')

    return render(request, 'shop/tracker.html')


def search(request):
    return render(request, 'shop/search.html')


def products(request, id):
    product = Product.objects.filter(id=id)
    return render(request, 'shop/products.html', {'product': product[0]})


def checkout(request):
    if(request.method == 'POST'):
        name = request.POST.get('name', '')
        items_json = request.POST.get('items_json', 'error')
        phone = request.POST.get('phone', '')
        email = request.POST.get('email', '')
        city = request.POST.get('city', '')
        state = request.POST.get('state', '')
        address = request.POST.get('address1', '') + \
            request.POST.get('address2', '')
        zip_code = request.POST.get('zip_code', '')

        
        order = Order(items_json=items_json, name=name, email=email, address=address,
                      city=city, state=state, zip_code=zip_code, phone=phone)
        order.save()
        update = OrderUpdate(
            order_id=order.id, update_desc="The Order has been placed")
        update.save()
        return render(request, 'shop/checkout.html', {'thank': True, 'id': order.id})
    return render(request, 'shop/checkout.html', {'thank': False})


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
    myprod.save()"""
