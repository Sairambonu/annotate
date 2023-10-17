from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from users.models import UserLoginInfo
from django.contrib import messages
from django.http import JsonResponse
from django.conf import settings
from .models import Datasets,AnnotateLanguageUsers
from django.core import serializers
import ast
from .utils import *
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def index(request):
	return redirect('display')


def upload(request):
	if request.method=='POST':
		file = request.FILES.get('upload')
		language = request.POST.get('languageSelect')
		task_name = request.POST.get('task_name')
		set_name = request.POST.get('set_name')
		user_email = request.POST.get('user_email')
		deadline = request.POST.get('deadline')
		status = request.POST.get('status')
		filename = file.name
		json_path = str(settings.BASE_DIR)+ "/static/datasets/"+str(filename)
		if hasattr(request, "user"):
			use_email = request.user.email
		else:
			messages.info(request, "User session expired.!")
		
		
		if use_email is not None:
			if path.exists(json_path):
				messages.error(request, 'file already exists')
				return render(request,'anno/upload.html')
			else:
				datas = read_jsonl_str(file)
				checkfile = write_as_jsonl(json_path,datas,order_display=True)
				if checkfile:
					Datasets.objects.create(dataset_path=filename, language=language, 
						task_name=task_name, set_name=set_name, user_email=user_email, 
						deadline=deadline)

					messages.success(request, 'File stored successfully!')
					return redirect('display')
				else:
					messages.error(request, 'File storage failed!')
			return render(request,'anno/upload.html')
		else:
			messages.info(request, "User session expired.!")
	return render(request,'anno/upload.html',)

def display(request):
	return render(request,'anno/display.html')

def get_emails(request):
    selected_language = request.GET.get('language', '')  # Get the selected language from the request

    # Query the database to get emails based on the selected language
    # if selected_language:
    #     user_emails = UserLoginInfo.objects.filter(languages__contains=[selected_language]).values_list('email', flat=True)
    # else:
    #     user_emails = []
    user_emails = []
    object_list = serializers.serialize("python", UserLoginInfo.objects.all())
    for object in object_list:
    	entry = object.get('fields',{})
    	email = entry.get('email','')
    	language = ast.literal_eval(entry.get('languages', ''))
    	# user_emails.append(language)
    	for lang in language:
    		if lang == selected_language:
    			user_emails.append(email)

    return JsonResponse({'user_emails':user_emails})

def predisplay(request, fileid):
	fileid = int(fileid)
	context ={}
	database_info = Datasets.objects.get(sno=fileid)
	filename = database_info.dataset_path
	json_path = str(settings.BASE_DIR)+ "/static/datasets/"+str(filename)
	context['articles'], implicit_check = read_jsonl(json_path, return_ids=True)
	context['implicit_check'] = implicit_check
	context['json_path'] = json_path
	request.session['json_path'] = json_path
	request.session['dataset_id'] = fileid
	data = context['articles']
	length = len(data)
	request.session['length'] = length

	return render(request, 'predisplay.html', context)

def nextpara(request,fileid):
	
	fileid = int(fileid)
	context ={}
	database_info = Datasets.objects.get(sno=fileid)
	filename = database_info.dataset_path
	json_path = str(settings.BASE_DIR)+ "/static/datasets/"+str(filename)
	datas, implicit_check = read_jsonl(json_path)
	
	
	context['implicit_check'] = implicit_check
	return JsonResponse({'datas':datas})

@csrf_exempt
def savecall(request):
	mrpairs = request.POST.get('mrpairs','')
	lrpairs = request.POST.get('lrpairs','')
	wb_display = request.POST.get('wb_display','')
	json_path = request.session.get('json_path', '')
	return save_data_back(mrpairs,lrpairs,json_path,wb_display)



def save_data_back(mrpairs, lrpairs, json_path, wb_display):
    try:
        data, implicit_check = read_jsonl(json_path)
        for i in range(len(data)):
            if wb_display == data[i]['set_id']:
                is_golden = data[i].get('is_golden', False)
                implicit_check = int(data[i].get('attempts', 0))
                output = data[i].get('output', {})

                if not output:
                    output = {
                        "lr_explanation": "",
                        "least_related": "",
                        "mr_explanation": "",
                        "most_related": ""
                    }

                no_check = implicit_check

                if is_golden:
                    if mrpairs != output["most_related"] and lrpairs != output["least_related"]:
                        no_check += 1

                if no_check > 5:
                    comments = 'you are distracted'
                else:
                    comments = ''

                data[i]['wb_display'] = wb_display
                data[i]['output'] = output
                data[i]['output']['most_related'] = mrpairs
                data[i]['output']['least_related'] = lrpairs
                data[i]['attempts'] = no_check
                data[i]['last_modified'] = strftime('%Y-%m-%d %H:%M:%S')
                data[i]['status'] = 'success'

                # Now, write the entire data list back to the file
                status = write_as_jsonl(json_path, data, order_display=False)

                if status:
                    return JsonResponse({'data': data[i]['output'], 'comments': comments})
                else:
                    return JsonResponse({'data': 'coudnt write'})

        # Handle the case where no matching item was found in the loop
        return JsonResponse({'status': 'pending', 'message': "Couldn't save successfully"})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})

