from django.shortcuts import render
from django.views.generic import TemplateView,CreateView,FormView,View
from .form import SkinDiseasesClassificationForm
import tensorflow.keras as K 
from tensorflow.keras.preprocessing import image
from tensorflow.keras.preprocessing.image import img_to_array 
import numpy as np 
from django.core.files.storage import default_storage
from .models import SkinDiseaseModel
from django.core.exceptions import ObjectDoesNotExist
from django.template.loader import get_template
from io import BytesIO
from xhtml2pdf import pisa
from django.http import HttpResponse
import datetime


class HomePageView(FormView):
    template_name = 'index.html'
    form_class = SkinDiseasesClassificationForm
    success_url = '/'

    def form_valid(self, form):
        predicted_class = form.predict()
        self.request.session['predicted_class'] = predicted_class[0]
        self.request.session['predicted_accuracy'] = predicted_class[1]
        # self.request.session['image_path'] = predicted_class[2]
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.session.get('predicted_class'):
            context['predicted_class'] =  self.request.session.get('predicted_class')
            context['predicted_accuracy'] = self.request.session.get('predicted_accuracy')
            # context['image_path'] = self.request.session['image_path']
            dis = SkinDiseaseModel.objects.get(name=context['predicted_class']) 
        # context['disease_name'] = dis.name
        # context['disease_definition'] = dis.definition
        # context['disease_reason'] = dis.reason
        # context['disease_solution'] = dis.solution
            if dis:
                context['dis'] = dis
            else:
                context['dis'] = None
        return context

class DownloadPDF(View):
    def get(self, request, *args, **kwargs):
        template_path = 'predict.html'
        context = {}
        context['predicted_class'] =  self.request.session.get('predicted_class')
        context['predicted_accuracy'] = self.request.session.get('predicted_accuracy')
            # context['image_path'] = self.request.session['image_path']
        dis = SkinDiseaseModel.objects.get(name=context['predicted_class'])
        context['dis'] = dis
        context['date_time'] = datetime.datetime.now() 
        # Render the template as a string
        html = get_template(template_path).render(context)
        # Generate the PDF
        pdf_file = BytesIO()
        pisa.CreatePDF(BytesIO(html.encode('utf-8')), pdf_file)
        # Set the Content-Disposition header to download the file
        response = HttpResponse(pdf_file.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{context["predicted_class"]}-report.pdf"'
        return response