from .models import IPAddress

class SaveIPAddressMiddleware:
    def __init__(self, get_responce):
        self.get_responce = get_responce  
        
    def __call__(self,request):
        x_forward_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forward_for:
            ip = x_forward_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        
        try:
            ip_address = IPAddress.objects.get(ip_address=ip)
        except IPAddress.DoesNotExist:
            ip_address = IPAddress(ip_address=ip)
            ip_address.save()
            
        request.user.ip_address = ip_address
        response = self.get_responce(request)
        
        
        return response