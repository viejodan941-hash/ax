from django.db import models

class DatasAx(models.Model):
    fecha = models.DateTimeField(auto_now_add=True)
    ip = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(null=True, blank=True)
    cookie = models.TextField(null=True, blank=True)
    data = models.TextField(null=True, blank=True)
    url_completa = models.TextField(null=True, blank=True)  # 👈 Con "a" al final
    
    def __str__(self):
        return f"Date {self.fecha} - IP: {self.ip}"
    
    class Meta:
        verbose_name = "Data Ax"
        verbose_name_plural = "Data Axs"
        ordering = ['-fecha']