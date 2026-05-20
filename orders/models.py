from django.db import models

class Order(models.Model):
    order_id = models.CharField(max_length=20, unique=True, blank=True)
    user_id = models.IntegerField()   # ✅ ADD THIS
    items = models.JSONField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.order_id:
            last = Order.objects.all().order_by('id').last()

            if last and last.order_id:
                number = int(last.order_id.replace("order", ""))
                number += 1
            else:
                number = 11

            self.order_id = f"order{number}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.order_id