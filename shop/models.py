from django.db import models

# Create your models here.
class Product(models.Model):
    product_id = models.AutoField
    product_name = models.CharField(max_length=50)
    category = models.CharField(max_length=50, default="")
    subcategory = models.CharField(max_length=50, default="")
    price = models.IntegerField(default=0)
    desc = models.CharField(max_length=1000)
    pub_date = models.DateField()
    image = models.ImageField(upload_to="shop/images", default="")

    def __str__(self) -> str:
        return self.product_name


class Contact(models.Model):
    msg_id = models.AutoField
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=10000, default='')
    phone = models.CharField(max_length=20, default='')
    query = models.CharField(max_length=10000, default='')
    
    def __str__(self) -> str:
        return "From => " + self.name

class Order(models.Model):
    order_id = models.AutoField
    items_json = models.CharField(max_length=5000, default="")
    amount = models.IntegerField(default=0)
    name = models.CharField(max_length=90)
    email = models.CharField(max_length=111)
    address = models.CharField(max_length=600)
    city = models.CharField(max_length=111)
    state = models.CharField(max_length=20)
    zip_code = models.CharField(max_length=6)
    phone = models.CharField(max_length=12)

class OrderUpdate(models.Model):
    update_id = models.AutoField
    order_id = models.IntegerField()
    update_desc = models.CharField(max_length=5000)
    timestamp = models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        print(self.update_desc)
        if len(self.update_desc) > 8:
            return self.update_desc[0:9] + "..."
        else:
            return self.update_desc
