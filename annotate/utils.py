from os import path, listdir, stat
import json
import ast
from django.core import serializers
# from TeluguTokenizer.summ_quality_check import *
from django.conf import settings
from .models import Datasets

SR_LABELS = ["set_id", "wb_display", "input", "output", "status", "start_time", "last_modified"]
SR_INPUT_LABELS = ["pair_id", "sentence_a", "sentence_b"]
SR_OUTPUT_LABELS = ["most_related", "least_related", "mr_explanation", "lr_explanation"]
SR_EXCLUDE_LABELS = ["is_golden", "attempts", "gold_output"]


def read_jsonl_str(uploaded_file):
    entries = []

    try:
        for line in uploaded_file.read().decode().splitlines():
            line = json.loads(line.strip())
            entries.append(line)
    except Exception as e:
        entries.append(e)

    return entries

def write_as_jsonl(out_filename, listOfDicts, order_display=False):
    try:
        with open(out_filename, 'w', encoding='utf-8') as outfile:
            wb_index = 1
            for each in listOfDicts:
                if order_display:
                    each['wb_display'] = str(wb_index)
                    each['status']=''
                json.dump(each, outfile, ensure_ascii=False)
                outfile.write('\n')
                wb_index += 1
            return True
    except Exception as e:
        return False
        

    

def read_jsonl(filename, return_ids=False, filter_ids=[], include_meta=False):
    entries = []
    implicit_check = 0

    for line in open(filename, 'r', encoding='utf-8'):
        line = json.loads(line)

        if 'metainfo' not in line and (len(filter_ids)==0 or str(line['set_id']) in filter_ids):
            line['wb_display'] = str(line['wb_display'])
            sample_status = line.get('status', '')

            ### Checking if the gold sentence is attempted or not.
            is_golden = line.get('is_golden', '')
            if is_golden=="true":
                attempts = line.get('attempts', '')
                if attempts=='':
                    attempts = 0
                    sample_status = ''
                elif int(attempts)==0:
                    attempts = 0
                    sample_status = 'success'
                else:
                    sample_status = 'success'
                if attempts>0:
                    implicit_check += 1

            # if len(line['wb_display'])==1:
            #     line['wb_display'] = "0"+ line['wb_display']
            if return_ids:
                entries.append({'wb_display': line['wb_display'], 'set_id': line['set_id'], 'status': sample_status})
            else:
                line['status'] = sample_status
                entries.append(line)
                
        elif 'metainfo' in line and include_meta:
            entries.append(line)
        
    return entries, implicit_check


def load_annotation_files(request):
    stats = []
    base = []
    datasets = Datasets.objects.all()  # Retrieve the model instances directly

    for dataset in datasets:
        user_check = False

        language = dataset.language
        sno = dataset.sno  # Access the primary key directly
        email = dataset.user_email
        task_name = dataset.task_name
        deadline = dataset.deadline
        status = dataset.status
        dataset_path = dataset.dataset_path
        last_updated = dataset.last_updated

        if email == request.user.email:
            user_check = True

        if user_check:
            base.append({'sno': sno, 'email': email, 'language': language,
                         'task_name': task_name, 'dataset_path': dataset_path, 'deadline': deadline, 
                         'status': status,'last_updated':last_updated})

    return base

# def load_annotation_files(request):
#     stats=[]
#     base=[]
#     object_list = serializers.serialize("python", Datasets.objects.all())

#     for object in object_list:
#         user_check = False

#         entry = object.get('fields','')
#         language = entry.get('language', '')
#         # sno = object.get('pk', '')
#         sno = object['pk']
#         email = entry.get('user_email','')
#         task_name = entry.get('task_name','')
#         deadline = entry.get('deadline','')
#         status = entry.get('status','')
#         dataset_path = entry.get('dataset_path','')

#         if entry.get('user_email','')==request.user.email:
#             user_check=True

#         if user_check==True:
#             base.append({'sno':entry.get('sno'),'email':email,'language':language,
#                 'task_name':task_name,'dataset_path':dataset_path,'deadline':deadline,'status':status})

#     return base

