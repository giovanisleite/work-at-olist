from django.db import models

from workatolist.phonecalls.pricing import calculate_price


class Call(models.Model):
    id = models.IntegerField(primary_key=True)
    started_at = models.DateTimeField(null=True)
    finished_at = models.DateTimeField(null=True)
    source = models.CharField(max_length=11, null=True)
    destination = models.CharField(max_length=11, null=True)

    price = models.FloatField(null=True, editable=False)

    class Meta:
        ordering = ['started_at', ]

    @property
    def duration(self):
        if self.started_at and self.finished_at:
            duration = (self.finished_at - self.started_at).total_seconds()
            hours = int(duration//3600)
            mins = int(duration % 3600//60)
            secs = int(duration % 3600 % 60)
            return f'{hours:d}h{mins:d}m{secs:d}s'
        return None

    def save(self, *args, **kwargs):
        if self.started_at and self.finished_at and not self.price:
            self.price = calculate_price(self.started_at, self.finished_at)
        super(Call, self).save(*args, **kwargs)
