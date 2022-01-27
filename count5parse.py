import json
import pandas as pd
from itertools import zip_longest

def counter5parse(input, output): 
    """
    Reads the Counter5 JSON file, selects the fields desctibed below by the 'cols' list
    and writes them as a csv file. 

    :param input: a string path to the raw JSON file
    :param output: a string path to the CSV file to be created
    """


    f = open(input)

    count5 = json.load(f)

    cols = ['platform', 
            'begin_date', 
            'end_date',
            'instance_total_item_investigations',
            'instance_unique_item_requests', 
            'instance_unique_item_investigations',
            'instance_total_item_requests',
            'instance_no_license',
            'item_id_doi',
            'item_id_proprietary',
            'item_id_online_ISSN',
            'item_id_print_ISSN',
            'title',
            'publisher_id_proprietary',
            'publisher',
            'data_type' ]

    d = {}

    for i in cols: 
        d[i] = [i]

    for i in range(0, len(count5['Report_Items'])):

        #Platform
        d['platform'].append(count5['Report_Items'][i]['Platform'])
        
        for j in range(0, len(count5['Report_Items'][i]['Performance'])):

        #begin_date
            try:     
                d['begin_date'].append(count5['Report_Items'][i]['Performance'][j]['Period']['Begin_Date'])
            except: 
                d['begin_date'].append('NA')

        #end_date
            try: 
                d['end_date'].append(count5['Report_Items'][i]['Performance'][j]['Period']['End_Date'])
            except:
                d['end_date'].append('NA')


            instSub = count5['Report_Items'][i]['Performance'][j]['Instance']

            for l in range(0, len(instSub)):

                    #instance_total_item_investigations
                    if instSub[l]['Metric_Type'] == 'Total_Item_Investigations':
                        try:
                            d['instance_total_item_investigations'].append(instSub[l]['Count'])
                        except: 
                            d['instance_total_item_investigations'].append('NA')

                    #instance_unique_item_requests
                    elif  instSub[l]['Metric_Type'] == 'Unique_Item_Requests': 
                        try:
                            d['instance_unique_item_investigations'].append(instSub[l]['Count'])
                        except: 
                            d['instance_unique_item_investigations'].append('NA')
                    
                    #instance_unique_item_investigations
                    elif  instSub[l]['Metric_Type'] == 'Unique_Item_Investigations':
                        try:
                            d['instance_unique_item_requests'].append(instSub[l]['Count'])
                        except: 
                            d['instance_unique_item_requests'].append('NA')

                    #instance_total_item_requests
                    elif instSub[l]['Metric_Type'] == 'Total_Item_Requests':
                        try: 
                            d['instance_total_item_requests'].append(instSub[l]['Count'])
                        except: 
                            d['instance_total_item_requests'].append('NA')
                    
                    #instance_no_license
                    elif  instSub[l]['Metric_Type'] == 'No_License':
                        try: 
                            d['instance_no_license'].append(instSub[l]['Count'])
                        except: 
                            d['instance_no_license'].append('NA')

        #DOI
            try: 
                d['item_id_doi'].append(count5['Report_Items'][i]['Item_ID'][0]['Value'])
            except: 
                d['item_id_doi'].append('NA')
        #Proprietary
            try:
                d['item_id_proprietary'].append(count5['Report_Items'][i]['Item_ID'][1]['Value'])
            except: 
                d['item_id_proprietary'].append('NA') 
        #Online_ISSN
            try:
                d['item_id_online_ISSN'].append(count5['Report_Items'][i]['Item_ID'][2]['Value'])
            except: 
                d['item_id_online_ISSN'].append('NA') 
        #Print_ISSN
            try:
                d['item_id_print_ISSN'].append(count5['Report_Items'][i]['Item_ID'][3]['Value'])
            except: 
                d['item_id_print_ISSN'].append('NA') 

        #Title
            try: 
                d['title'].append(count5['Report_Items'][i]['Title'])
            except: 
                d['title'].append('NA')
        
        #Publisher ID
            try: 
                d['publisher_id_proprietary'].append(count5['Report_Items'][i]['Publisher_ID'][0]['Value'])
            except: 
                d['publisher_id_proprietary'].append('NA')
        
        #Publisher
            try:
                d['publisher'].append(count5['Report_Items'][i]['Publisher'])
            except:
                d['publisher'].append('NA')
        
        #Data_Type
            try:
                d['data_type'].append(count5['Report_Items'][i]['Data_Type'])
            except:
                d['data_type'].append('NA')

    zl = list(zip_longest(*d.values()))
    df = pd.DataFrame(zl, columns=d.keys())

    df.to_csv(output, index=False, header =T)
