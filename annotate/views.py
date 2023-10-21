from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from users.models import UserLoginInfo
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from .models import Datasets,AnnotateLanguageUsers
from django.core import serializers
import ast
from .utils import *
import os
from time import gmtime, strftime
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def annotates(request):
	context = {}
	context['task_folders'] = load_annotation_files(request)
	return render (request,'anno/index.html',context)


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
					return redirect('manage_dataset')
				else:
					messages.error(request, 'File storage failed!')
			return render(request,'anno/upload.html')
		else:
			messages.info(request, "User session expired.!")
	return render(request,'anno/upload.html',)


def upload_update(request):
    context = {'telugu': [], 'hindi': [], 'marathi': []}

    if request.method == 'POST':
        if hasattr(request, "user"):
            use_email = request.user.email
        else:
            messages.info(request, "User session expired.")
            return render(request, 'anno/upload_update.html', context)  # Return early

        if use_email is not None:
            object_list = serializers.serialize('python', UserLoginInfo.objects.all())
            for object in object_list:
                entry = object.get('fields', {})
                user_email = entry.get('email', '')
                languages = ast.literal_eval(entry.get('languages', ''))
                for lang in languages:
                    if lang == 'telugu':
                        context['telugu'].append(user_email)
                    elif lang == 'hindi':
                        context['hindi'].append(user_email)
                    else:
                        context['marathi'].append(user_email)

    return render(request, 'anno/upload_update.html', context)



# def upload_update(request):
# 	context = {'telugu':[], 'hindi':[], 'marathi':[]}
# 	if request.method=='POST':
# 		context = {'telugu':[], 'hindi':[], 'marathi':[]}
# 		file = request.FILES.get('upload')
# 		language = request.POST.get('languageSelect')
# 		task_name = request.POST.get('task_name')
# 		set_name = request.POST.get('set_name')
# 		user_emails = request.POST.getlist('user_email')
# 		deadline = request.POST.get('deadline')
# 		status = request.POST.get('status')
# 		filename = file.name
# 		json_path = str(settings.BASE_DIR)+ "/static/datasets/"+str(filename)
# 		if hasattr(request, "user"):
# 			use_email = request.user.email
# 		else:
# 			messages.info(request, "User session expired.!")
		
		
# 		if use_email is not None:
# 			object_list = serializers.serialize('python', UserLoginInfo.objects.all())
# 			for object in object_list:
# 				entry = object.get('fields',{})
# 				user_email = entry.get('user_email','')
# 				languages = ast.literal_eval(entry.get('languages', ''))
# 				for lang in languages:
# 					if lang=='telugu':
# 						context['telugu'].append(user_email)
# 					elif lang=='hindi':
# 						context['hindi'].append(user_email)
# 					else:
# 						context['marathi'].append(user_email)
# 			user_emails = ast.literal_eval(user_emails)
# 			for email in user_emails:
# 				datas = read_jsonl_str(file)
# 				checkfile = write_as_jsonl(json_path,datas,order_display=True)
# 				if checkfile:
# 					Datasets.objects.create(dataset_path=filename, language=language, 
# 						task_name=task_name, set_name=set_name, user_email=email, 
# 						deadline=deadline)

# 			return render(request,'anno/upload_update.html', context)
# 		else:
# 			messages.info(request, "User session expired.!")
# 	return render(request,'anno/upload_update.html', context)


# def upload_update(request):
#     context = {'telugu': [], 'hindi': [], 'marathi': []}

#     if request.method == 'POST':
#         file = request.FILES.get('upload')
#         language = request.POST.get('languageSelect')
#         task_name = request.POST.get('task_name')
#         set_name = request.POST.get('set_name')
#         user_emails = request.POST.getlist('user_email')
#         deadline = request.POST.get('deadline')
#         status = request.POST.get('status')
#         filename = file.name
#         json_path = os.path.join(settings.BASE_DIR, "static", "datasets", filename)

#         if request.user.is_authenticated:
#         	logged_in_user_email = request.user.email
#         else:
#         	messages.info(request, "User session expired.")
#         	return render(request, 'anno/upload_update.html', context)


#         object_list = UserLoginInfo.objects.all()
#         for obj in object_list:
#         	user_email = obj.email
#         	languages = obj.languages
#         	if 'telugu' in languages:
#         		context['telugu'].append(user_email)
#         	elif 'hindi' in languages:
#         		context['hindi'].append(user_email)
#         	else:
#         		context['marathi'].append(user_email)

#         if logged_in_user_email:
#         	datas = read_jsonl_str(file)
#         	checkfile = write_as_jsonl(json_path, datas, order_display=True) 
#         	if checkfile:
#         		for email in user_emails:
#         			Datasets.objects.create(
#         				dataset_path=filename,
#         				language=language,
#         				task_name=task_name,
#         				set_name=set_name,
#         				user_email=email,
#         				deadline=deadline
#         			)
#         		return redirect('display')
#         	else:
#         		messages.info(request, "User session expired.")

#     return render(request,'anno/upload_update.html', context)
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

	return render(request, 'anno/predisplay.html', context)

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
	dataset_id = request.session.get('dataset_id')

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


@csrf_exempt
def download_data(request, dataset_id):
	dataset_id = int(dataset_id)

	dataset_entry = Datasets.objects.get(sno = dataset_id)
	json_path = str(settings.BASE_DIR)+ "/static/datasets/" + str(dataset_entry.dataset_path)

	if os.path.exists(json_path):
		json_data, implicit_check = read_jsonl(json_path, include_meta=True)

		json_data_str = ''
		for line in json_data:
			line = json.dumps(line, ensure_ascii=False)
			json_data_str += line + "\n"

		print("Date Time: ", strftime("%Y-%m-%d_%H-%M-%S"))
		output_file_name = strftime("%Y-%m-%d_%H-%M-%S") + "_" + os.path.basename(json_path)

		response = HttpResponse(json_data_str, content_type="application/vnd.ms-excel")
		response['Content-Disposition'] = 'inline; filename=' + output_file_name 
		return response
	
	raise Http404

def manage_datasets(request):
	context={}
	base=[]
	username = request.user.username
	if username is not None:
		coord = UserLoginInfo.objects.get(username=username)
		coord_langs = coord.languages
		languages = ast.literal_eval(coord_langs)
		object_list = serializers.serialize("python", Datasets.objects.all())
		Telugu= None
		Hindi = None
		Marathi = None
		for lang in languages:
			if lang =='telugu':
				Telugu=lang
			elif lang=='hindi':
				Hindi=lang
			elif lang=='marathi':
				Marathi==lang

		if Telugu is not None and Hindi is not None and Marathi is not None:
			user_details = {}
			for object in object_list:
				entry = object.get('fields','')
				sno = object.get('pk','')
				if entry.get('language')==Telugu or entry.get('language')==Hindi or entry.get('language')==Hindi:
					username = object.get('user_email')
					dataset_path = entry.get('dataset_path')
					task_name =entry.get('task_name')
					set_name =entry.get('set_name')
					deadline =entry.get('deadline')
					last_updated =entry.get('last_updated')
					if username not in user_details:
						user_details[username] = {'username':username,'dataset_path':dataset_path,
						'task_name':task_name,'set_name':set_name,'deadline':deadline,
						'last_updated':last_updated,'sno':sno,}
					if user_details[username]['sno']<sno:
						user_details[username] = {'username':username,'dataset_path':dataset_path,
						'task_name':task_name,'set_name':set_name,'deadline':deadline,
						'last_updated':last_updated,'sno':sno,}
			context['task_folders']=user_details.values()
			return render(request,'manage_dataset.html',context)


		elif Telugu is not None and Hindi is not None and Marathi is None:
			user_details = {}
			for object in object_list:
				entry = object.get('fields','')
				if entry.get('language')==Telugu or entry.get('language')==Hindi:
					username = entry.get('user_email')
					dataset_path = entry.get('dataset_path')
					task_name =entry.get('task_name')
					set_name =entry.get('set_name')
					deadline =entry.get('deadline')
					last_updated =entry.get('last_updated')
					if username not in user_details:
						user_details[username] = {'username':username,'dataset_path':dataset_path,
						'task_name':task_name,'set_name':set_name,'deadline':deadline,
						'last_updated':last_updated,'sno':sno,}
					if user_details[username]['sno']<sno:
						user_details[username] = {'username':username,'dataset_path':dataset_path,
						'task_name':task_name,'set_name':set_name,'deadline':deadline,
						'last_updated':last_updated,'sno':sno,}
			context['task_folders']=user_details.values()
			return render(request,'manage_dataset.html',context)

		if Telugu is not None and Hindi is None and Marathi is not None:
			user_details = {}
			for object in object_list:
				entry = object.get('fields','')
				sno = object.get('pk', '')
				if entry.get('language')==Telugu or entry.get('language')==Marathi:
					username = entry.get('user_email')
					dataset_path = entry.get('dataset_path')
					task_name =entry.get('task_name')
					set_name =entry.get('set_name')
					deadline =entry.get('deadline')
					last_updated =entry.get('last_updated')
					base.append({'username':username,'dataset_path':dataset_path,
						'task_name':task_name,'set_name':set_name,'deadline':deadline,
						'last_updated':last_updated,'sno': sno})
			context['task_folders']=user_details.values()
			return render(request,'manage_dataset.html',context)
		elif Telugu is None and Hindi is not None and Marathi is not None:
			user_details = {}
			for object in object_list:
				entry = object.get('fields','')
				if entry.get('language')==Hindi or entry.get('language')==Marathi:
					username = entry.get('user_email')
					dataset_path = entry.get('dataset_path')
					task_name =entry.get('task_name')
					set_name =entry.get('set_name')
					deadline =entry.get('deadline')
					last_updated =entry.get('last_updated')
					if username not in user_details:
						user_details[username] = {'username':username,'dataset_path':dataset_path,
						'task_name':task_name,'set_name':set_name,'deadline':deadline,
						'last_updated':last_updated,'sno':sno,}
					if user_details[username]['sno']<sno:
						user_details[username] = {'username':username,'dataset_path':dataset_path,
						'task_name':task_name,'set_name':set_name,'deadline':deadline,
						'last_updated':last_updated,'sno':sno,}
			context['task_folders']=user_details.values()
			return render(request,'manage_dataset.html',context)
		elif Telugu is not None and Hindi is None and Marathi is None:
			user_details = {}
			for object in object_list:
				entry = object.get('fields','')
				sno = object.get('pk','')
				if entry.get('language')==Telugu:
					username = entry.get('user_email')
					dataset_path = entry.get('dataset_path')
					task_name =entry.get('task_name')
					set_name =entry.get('set_name')
					deadline =entry.get('deadline')
					last_updated =entry.get('last_updated')
					if username not in user_details:
						user_details[username] = {'username':username,'dataset_path':dataset_path,
						'task_name':task_name,'set_name':set_name,'deadline':deadline,
						'last_updated':last_updated,'sno':sno,}
					if user_details[username]['sno']<sno:
						user_details[username] = {'username':username,'dataset_path':dataset_path,
						'task_name':task_name,'set_name':set_name,'deadline':deadline,
						'last_updated':last_updated,'sno':sno,}
					# base.append({'username':username,'dataset_path':dataset_path,
					# 	'task_name':task_name,'set_name':set_name,'deadline':deadline,
					# 	'last_updated':last_updated,'sno':sno,})
			context['task_folders']=user_details.values()
			return render(request,'manage_dataset.html',context)
		elif Telugu is None and Hindi is not None and Marathi is None:
			for object in object_list:
				entry = object.get('fields','')
				if entry.get('language')==Hindi:
					username = entry.get('user_email')
					dataset_path = entry.get('dataset_path')
					task_name =entry.get('task_name')
					set_name =entry.get('set_name')
					deadline =entry.get('deadline')
					last_updated =entry.get('last_updated')
					if username not in user_details:
						user_details[username] = {'username':username,'dataset_path':dataset_path,
						'task_name':task_name,'set_name':set_name,'deadline':deadline,
						'last_updated':last_updated,'sno':sno,}
					if user_details[username]['sno']<sno:
						user_details[username] = {'username':username,'dataset_path':dataset_path,
						'task_name':task_name,'set_name':set_name,'deadline':deadline,
						'last_updated':last_updated,'sno':sno,}
			context['task_folders']=user_details.values()
			return render(request,'manage_dataset.html',context)
		elif Telugu is None and Hindi is None and Marathi is not None:
			for object in object_list:
				entry = object.get('fields','')
				if entry.get('language')==Marathi:
					username = entry.get('user_email')
					dataset_path = entry.get('dataset_path')
					task_name =entry.get('task_name')
					set_name =entry.get('set_name')
					deadline =entry.get('deadline')
					last_updated =entry.get('last_updated')
					if username not in user_details:
						user_details[username] = {'username':username,'dataset_path':dataset_path,
						'task_name':task_name,'set_name':set_name,'deadline':deadline,
						'last_updated':last_updated,'sno':sno,}
					if user_details[username]['sno']<sno:
						user_details[username] = {'username':username,'dataset_path':dataset_path,
						'task_name':task_name,'set_name':set_name,'deadline':deadline,
						'last_updated':last_updated,'sno':sno,}
			context['task_folders']=user_details.values()
			return render(request,'manage_dataset.html',context)




