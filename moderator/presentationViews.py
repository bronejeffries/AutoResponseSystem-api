import os
from django.http import HttpResponse
from django.shortcuts import render
from pptx import Presentation
from Ars.decorators import Get_check,Post_check
import io, random
from pptx.chart.data import CategoryChartData
from pptx.enum.chart import XL_CHART_TYPE
from pptx.util import Inches
from Ars.models import Session, Topic, Question
# from .categoryViews import get_Question

def generate_random():
    return random.randint(1, 1001)

def get_Question(pk):
    question = None
    try:
        question = Question.objects.get(id=pk)
    except Question.DoesNotExist:
        return False
    else:
        return question

def question_options(question):
     options = question.option_set.all()
     return options

def makeQuestionPresentation(question_id, name = None):
    # path
    presentation_name = ""
    if name is not None:
        presentation_name = name
    else:
        presentation_name = str(question_id)+ "_" + str(generate_random())

    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    storage_path = os.path.join(BASE_DIR, 'moderator/presentations')
    presentation_path = os.path.join(storage_path, presentation_name + '.pptx')
    # create presentation with one slide
    prs = Presentation()
    slide = prs.slides.add_slide(prs.slide_layouts[5])

    # define chart bar data
    chart_data = CategoryChartData()
    question = get_Question(question_id)
    question_options_choices = None
    question_options_list = None
    if question:
        question_options_list = question_options(question)
        question_options_choices = [option.choices for option in question_options_list]

    chart_data.categories = [ n+1 for n in range(len(question_options_list)) ]
    chart_data.add_series('series 1', tuple(question_options_choices))

    # add chart to slide
    x, y, cx, cy = Inches(2), Inches(2), Inches(6), Inches(4.5)
    slide.shapes.add_chart(
        XL_CHART_TYPE.COLUMN_CLUSTERED, x, y, cx, cy, chart_data
    )
    prs.save(presentation_path)
    return (prs , presentation_name)

@Get_check
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
