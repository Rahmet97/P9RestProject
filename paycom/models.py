from django.db import models


from django.db import models


class Transaction(models.Model):

    class Status(models.TextChoices):
        PROCESS = 0, 'processing'
        PAID = 1, 'paid'
        FAILED = 2, 'failed'

    trans_id = models.CharField(max_length=255)
    request_id = models.IntegerField()
    amount = models.DecimalField(decimal_places=2, default=0.00, max_digits=10)
    account = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, default=Status.PROCESS, choices=Status.choices)
    create_time = models.DateTimeField(auto_now_add=True)
    pay_time = models.DateTimeField(auto_now=True)


    def create_transaction(self, trans_id, request_id, amount, account, status):
        Transaction.objects.create(
            trans_id=trans_id,
            request_id=request_id,
            amount=amount / 100,
            account=account,
            status=status
        )

    def update_transaction(self, trans_id, status):
        trans = Transaction.objects.get(trans_id=trans_id)
        trans.status = status
        trans.save()
