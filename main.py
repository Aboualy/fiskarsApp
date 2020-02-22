import numpy as np
import pandas as pd
import glob

def read_csv_file(filename):
    #reading each CSV file as a Pandas dataframe
    df = pd.read_csv(filename)
    #merging all the values into  one column
    df['values'] = df[df.columns[4:]].apply( lambda x: ''.join(x.dropna().astype(str)), axis=1).astype(float)
    df = (df.pivot_table(index="store",columns="kpi", values='values', aggfunc='mean')
            .rename_axis(None, axis=1)
            .reset_index())
    #get the date from the directory name
    date =  filename.split('/')[1].strip()
    df.insert(loc=0, column='date', value=date)
    return df

def read_all_csv_files(path):
    """
    opening all directories in 'store_kpi', then converting each CSV file in each directory into a dataframe (as a row)
    append that row into the main dataframe that has all the CSV files
    """
    index = 0
    dataframe = pd.DataFrame(columns=['date', 'store', 'Avg daily sales', 'Basket size, pieces',
           'Basket size, value', 'Days open', 'Margin, value', 'Receipts', 'Sales',
           'Visitors'])

    for filename in glob.glob(path):
        df = read_csv_file(filename)
        dataframe.loc[index] = np.array(df).ravel()
        index += 1
    return dataframe

def save_df_to_csv(df):
    """
    saving the final data frame as a CSV, nder the name of 'result.csv'
    """
    with open('result.csv', 'w') as filetowrite:
        df.to_csv(filetowrite, sep='\t', encoding='utf-8', index=False)



if __name__ == "__main__":
    df = read_all_csv_files("/Users/aboualy/Downloads/store_kpi/*/*.csv")
    save_df_to_csv(df)
    # the average Margin, value of store 1050
    average_margin = df[df['store'] == 1050]['Margin, value'].mean()
    # output: 218666.7037037037
    print('The average_margin is: {:0.2f}'.format(average_margin))
    # the highest Sales of store 1071 (both date and amount)
    highest_sales = df.iloc[df.index[df['Sales'] == df[df['store'] == 1071]['Sales'].max()]][
        ['date', 'store', 'Sales']]
    print(highest_sales.head())
    print('The highest Sales of store 1071 (date) is: ', highest_sales.date.values[0])
    print('The highest Sales of store 1071 (amount) is: {:.0f}'.format(highest_sales.Sales.values[0]))
    # the average of all KPI of store 1066
    print(df[df['store'] == 1066].mean())