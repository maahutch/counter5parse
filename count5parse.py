import pandas as pd
import json

def counter5parse(input):     
    """
    Reads the Counter5 JSON file and selects the following fields:

    Platform, 
    Title, 
    Publisher, 
    DataType, 
    Begin_Date, 
    End_Date,
    Total_Item_Investigations,
    Unique_Item_Requests,
    Unique_Item_Investigations,
    Total_Item_Requests,
    DOI	Proprietary,
    Online_ISSN,
    Print_ISSN,
    No_License

    The function returns a denormalized pandas dataframe.  

    :param input: a string path to the raw JSON file
    """

    f = open(input)

    count5 = json.load(f)

    df = pd.json_normalize(count5)

    x = pd.DataFrame(df).T.apply(pd.Series.explode).rename_axis('Title').reset_index()

    x = x[x['Title'] == 'Report_Items']

    x = x.rename(columns={0:'data'})


    x = pd.DataFrame(x['data'].tolist())


    counter5 = pd.DataFrame()

    for index, row in x.iterrows():

        oneRow = dict(row)

        output = [{'Platform': oneRow['Platform'],
                    'Title':   oneRow['Title'],
                    'Publisher': oneRow['Publisher'],
                    'DataType': oneRow['Data_Type']
                    }]

        outDF = pd.DataFrame(output)

        date = pd.DataFrame()
        metricDF = pd.DataFrame()

        for i in range(0, len(oneRow['Performance'])):
            date = date.append(pd.DataFrame(pd.Series(oneRow['Performance'][0]['Period'])).T)

            metric = oneRow['Performance'][i]['Instance']
            metricMod = dict(d.values() for d in metric)
            oneMetricDF  = pd.DataFrame(metricMod, index = [0])
            metricDF = metricDF.append(oneMetricDF)


        date = pd.concat([date.reset_index(drop=True),
                            metricDF.reset_index(drop=True)], axis=1)
        
        outDF = outDF.merge(date, how='cross')


        id = oneRow['Item_ID']
        idMod = dict(d.values() for d in id)
        oneIdDF = pd.DataFrame(idMod, index = [0])
        
        outDF = outDF.merge(oneIdDF, how='cross')

        counter5 = counter5.append(outDF)
    
    return(counter5)
    
    

if __name__ == "__main__":
    out = counter5parse('rawCat5.json')

    out.to_csv('output.csv', index=False, header = True)