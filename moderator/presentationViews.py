import os
from django.http import HttpResponse
from django.shortcuts import render
from pptx import Presentation
from Ars.decorators import Get_check,Post_check
import io

def getPresentation(request,name):
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    storage_path = os.path.join(BASE_DIR, 'moderator/presentations')
    presentation_path = os.path.join(storage_path, name + '.pptx')
    # file = open(presentation_path)
    # prs = Presentation(presentation_path)
    # file.close()
    targetstream = io.BytesIO()
    with open(presentation_path,'rb') as f:
        targetstream = io.BytesIO(f.read())
    # prs.save(targetstream)
    response = HttpResponse(content_type='application/vnd.ms-powerpoint')
    response['Content-Disposition'] = 'attachment; filename="'+name+'.pptx"'
    response.write(targetstream.getvalue())
    targetstream.close()
    return response

@Get_check
def viewPresentation(request,name):
    scheme = request.is_secure() and "https" or "http"
    pathheader = scheme+"://"+request.META['HTTP_HOST']
    return render(request,'moderator/viewpresentation.html',{'presentationname':name,'pathheader':pathheader})
