from django.db import models
from datetime import datetime


class Staff(models.Model):
    full_name = models.CharField(max_length=255)
    position = models.CharField(max_length=255)
    labor_contract = models.IntegerField()

    def get_last_name(self):
        return self.full_name.split()[0]


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField(default=0.0)
    composition = models.TextField(default="Состав не указан")


class Order(models.Model):
    time_in = models.DateTimeField(auto_now_add=True)
    time_out = models.DateTimeField(null=True)
    cost = models.FloatField(default=0.0)
    take_away = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    staff = models.ForeignKey(Staff, on_delete=models.CASCADE)

    products = models.ManyToManyField(Product, through='ProductOrder')

    def finish_order(self):
        self.time_out = datetime.now()
        self.complete = True
        self.save()

    def get_duration(self):
        if self.complete:  # если завершен, возвращаем разность объектов
            return (self.time_out - self.time_in).total_seconds() // 60
        else:  # если еще нет, то сколько длится выполнение
            return (datetime.now() - self.time_in).total_seconds() // 60


class ProductOrder(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    _amount = models.IntegerField(default=1, db_column = 'amount')

    def product_sum(self):
        product_price = self.product.price
        return product_price * self.amount

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        self._amount = int(value) if value >= 0 else 0
        self.save()


cap = Product(name = "Капучино 0.3", price = 99.0)
cap.save()
cap_big = Product.objects.create(name = "Капучино 0.4", price = 109.0)

cap = Product(name = "Картофель фри (станд.)", price = 93.0)
cap.save()
cap_big = Product.objects.create(name = "Картофель фри (бол.)", price = 106.0)

cashier1 = Staff.objects.create(full_name="Иванов Иван Иванович",
                                position=Staff.cashier,
                                labor_contract=1754)
cashier2 = Staff.objects.create(full_name="Петров Петр Петрович",
                                position=Staff.cashier,
                                labor_contract=4355)
direct = Staff.objects.create(full_name="Максимов Максим Максимович",
                              position=Staff.director,
                              labor_contract=1254)