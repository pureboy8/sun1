from django.shortcuts import render,get_object_or_404
from .models import BlogAriticles
import  os
# Create your views here.

def blog_title(request):
    blogs=BlogAriticles.objects.all()
    return render(request,"blog/title.html",{"blogs":blogs})

def blog_article(request,article_id):
    #article=BlogAriticles.objects.get(id=article_id)
    article=get_object_or_404(BlogAriticles,id=article_id)
    pub=article.publish
    import qrcode
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(article.title)
    qr.make(fit=True)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(os.path.join(BASE_DIR,'static/imgs/a.png'))
    return render(request,"blog/content.html",{"article":article,"publish":pub })