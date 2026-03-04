from .models import Social

def get_social_links(request):
    socials = Social.objects.all()
    return {
        'social_links' : socials
    }