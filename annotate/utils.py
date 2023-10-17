from os import path, listdir, stat
import json
from django.core import serializers
# from TeluguTokenizer.summ_quality_check import *
from django.conf import settings

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
