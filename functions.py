import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def display_plot_target(data, col, size=(12,7)):    
    fig, ax = plt.subplots(figsize=size)

    # KDE plot of loans that were repaid on time
    sns.kdeplot(data.loc[data['TARGET'] == 0, col], label = 'target == 0')

    # KDE plot of loans which were not repaid on time
    sns.kdeplot(data.loc[data['TARGET'] == 1, col], label = 'target == 1')

    ax.legend(wedges, leg,
              loc="center left",
              fontsize = 'x-large',
              bbox_to_anchor=(1, 0, 0.5, 1))
    # Labeling of plot
    plt.xlabel(col)
    plt.ylabel('Densité')
    plt.title('Distribution de {}'.format(col), fontsize=20)
    plt.show()
    
def feature_type_split(data):
    cat_list = []
    dis_num_list = []
    num_list = []
    for i in data.columns.tolist():
        if data[i].dtype.name == 'category':
            cat_list.append(i)
        elif data[i].nunique() < 25:
            dis_num_list.append(i)
        else:
            num_list.append(i)
    return cat_list, dis_num_list, num_list

def cat(chaine, dictionnaire):
    tag = 'Other'
    for cle in dictionnaire:
        if cle in str(chaine):
            tag = dictionnaire[cle]
            break
    return tag

def category(df):
    
    for c in df.columns:
        col_type = df[c].dtype
        if col_type == 'object' or col_type.name == 'category':
            df[c] = df[c].astype('category')
    return df
        
    
def agg_numeric(df, group_var, df_name):
    """Aggregates the numeric values in a dataframe. This can
    be used to create features for each instance of the grouping variable.
    
    Parameters
    --------
        df (dataframe): 
            the dataframe to calculate the statistics on
        group_var (string): 
            the variable by which to group df
        df_name (string): 
            the variable used to rename the columns
        
    Return
    --------
        agg (dataframe): 
            a dataframe with the statistics aggregated for 
            all numeric columns. Each instance of the grouping variable will have 
            the statistics (mean, min, max, sum; currently supported) calculated. 
            The columns are also renamed to keep track of features created.
    
    """
    # Remove id variables other than grouping variable
    for col in df:
        if col != group_var and 'SK_ID' in col:
            df = df.drop(columns = col)
            
    group_ids = df[group_var]
    numeric_df = df.select_dtypes('number')
    numeric_df[group_var] = group_ids

    # Group by the specified variable and calculate the statistics
    agg = numeric_df.groupby(group_var).agg(['count', 'mean', 'max', 'min', 'sum']).reset_index()

    # Need to create new column names
    columns = [group_var]

    # Iterate through the variables names
    for var in agg.columns.levels[0]:
        # Skip the grouping variable
        if var != group_var:
            # Iterate through the stat names
            for stat in agg.columns.levels[1][:-1]:
                # Make a new column name for the variable and stat
                columns.append('%s_%s_%s' % (df_name.upper(), var.upper(), stat.upper()))

    agg.columns = columns
    return agg

def count_categorical(df, group_var, df_name):
    """Computes counts and normalized counts for each observation
    of `group_var` of each unique category in every categorical variable
    
    Parameters
    --------
    df : dataframe 
        The dataframe to calculate the value counts for.
        
    group_var : string
        The variable by which to group the dataframe. For each unique
        value of this variable, the final dataframe will have one row
        
    df_name : string
        Variable added to the front of column names to keep track of columns

    
    Return
    --------
    categorical : dataframe
        A dataframe with counts and normalized counts of each unique category in every categorical variable
        with one row for every unique value of the `group_var`.
        
    """
    
    # Select the categorical columns
    categorical = pd.get_dummies(df.select_dtypes('object'))

    # Make sure to put the identifying id on the column
    categorical[group_var] = df[group_var]

    # Groupby the group var and calculate the sum and mean
    categorical = categorical.groupby(group_var).agg(['sum', 'mean'])
    
    column_names = []
    
    # Iterate through the columns in level 0
    for var in categorical.columns.levels[0]:
        # Iterate through the stats in level 1
        for stat in ['count', 'count_norm']:
            # Make a new column name
            column_names.append('%s_%s_%s' % (df_name.upper(), var.upper(), stat.upper()))
    
    categorical.columns = column_names
    
    return categorical

# Fonction qui calcule les données manquantes
def missing_values_table(df):
    # Total données manquantes
    mis_val = df.isnull().sum()
        
    # Pourcentage données manquantes
    mis_val_percent = 100 * df.isnull().sum() / len(df)
        
    # Tableau avec les résultats
    mis_val_table = pd.concat([mis_val, mis_val_percent], axis=1)
        
    # Renomme les colonnes
    mis_val_table_ren_columns = mis_val_table.rename(
    columns = {0 : 'Valeurs manquantes', 1 : '% Total Données'})
        
    # Classement en fonciton du pourcentage de données manquantes
    mis_val_table_ren_columns = mis_val_table_ren_columns[
        mis_val_table_ren_columns.iloc[:,1] != 0].sort_values(
    '% Total Données', ascending=False).round(1)
        
    # Affichage des infos résumés
    print ("Le dataframe a " + str(df.shape[1]) + " colonnes.\n"      
        "Il contient " + str(mis_val_table_ren_columns.shape[0]) +
            " colonnes avec des données manquantes.")
        
    # Retourne le tableau sur les données manquantes
    return mis_val_table_ren_columns

def col_to_remove(df):
    corrs = df.corr()
    corrs = corrs.sort_values('TARGET', ascending = False)
    # Set the threshold
    threshold = 0.8

    # Empty dictionary to hold correlated variables
    above_threshold_vars = {}

    # For each column, record the variables that are above the threshold
    for col in corrs:
        above_threshold_vars[col] = list(corrs.index[corrs[col] > threshold])

    # Track columns to remove and columns already examined
    cols_to_remove = []
    cols_seen = []
    cols_to_remove_pair = []

    # Iterate through columns and correlated columns
    for key, value in above_threshold_vars.items():
        # Keep track of columns already examined
        cols_seen.append(key)
        for x in value:
            if x == key:
                next
            else:
                # Only want to remove one in a pair
                if x not in cols_seen:
                    cols_to_remove.append(x)
                    cols_to_remove_pair.append(key)

    cols_to_remove = list(set(cols_to_remove))
    print('Nombre de colonnes à supprimer: ', len(cols_to_remove))
    
    return df.drop(columns = cols_to_remove)

def total_cleaning(df, bureau, bureau_balance, cols_to_remove):
    df['TERM'] = df.AMT_CREDIT / df.AMT_ANNUITY
    df['OVER_EXPECT_CREDIT'] = (df.AMT_CREDIT > df.AMT_GOODS_PRICE).map({False:0, True:1})
    
    flag_doc_index = df.iloc[:,df.columns.str.startswith('FLAG_DOCUMENT_')].columns.tolist()
    df['FLAG_DOCUMENT_TOTAL'] = df.loc[:,flag_doc_index].sum(axis=1)
    df.drop(columns=flag_doc_index, inplace=True)
    req_index = df.iloc[:,df.columns.str.startswith('AMT_REQ_CREDIT_BUREAU_')].columns.tolist()
    df['AMT_REQ_CREDIT_BUREAU_TOTAL'] = df.loc[:, req_index].sum(axis=1)
    df.drop(columns=req_index, inplace=True)
    
    df['BIRTH_EMPLOTED_INTERVEL'] = df.DAYS_BIRTH / -365 - df.DAYS_EMPLOYED / -365
    
    df['BIRTH_EMPLOTED_INTERVEL'] = df.DAYS_BIRTH / -365 - df.DAYS_EMPLOYED / -365
    df['BIRTH_REGISTRATION_INTERVEL'] = df.DAYS_REGISTRATION - df.DAYS_BIRTH
    
    df['INCOME_PER_FAMILY_MEMBER'] = df.AMT_INCOME_TOTAL / df.CNT_FAM_MEMBERS
    
    previous_loan_counts = bureau.groupby('SK_ID_CURR', as_index=False)['SK_ID_BUREAU'].count().rename(columns = {'SK_ID_BUREAU': 'CNT_PREV_LOAN'})
    
    bureau_counts = count_categorical(bureau, group_var = 'SK_ID_CURR', df_name = 'bureau')
    bureau_agg = agg_numeric(bureau.drop(columns = ['SK_ID_BUREAU']), group_var = 'SK_ID_CURR', df_name = 'bureau')
    bureau_balance_counts = count_categorical(bureau_balance, group_var = 'SK_ID_BUREAU', df_name = 'bureau_balance')
    bureau_balance_agg = agg_numeric(bureau_balance, group_var = 'SK_ID_BUREAU', df_name = 'bureau_balance')
    
    # Dataframe grouped by the loan
    bureau_by_loan = bureau_balance_agg.merge(bureau_balance_counts, right_index = True, left_on = 'SK_ID_BUREAU', how = 'outer')

    # Merge to include the SK_ID_CURR
    bureau_by_loan = bureau[['SK_ID_BUREAU', 'SK_ID_CURR']].merge(bureau_by_loan, on = 'SK_ID_BUREAU', how = 'left')

    # Aggregate the stats for each client
    bureau_balance_by_client = agg_numeric(bureau_by_loan.drop(columns = ['SK_ID_BUREAU']), group_var = 'SK_ID_CURR', df_name = 'client')
    
    # Merge with the value counts of bureau
    df = df.merge(bureau_counts, on = 'SK_ID_CURR', how = 'left')

    # Merge with the stats of bureau
    df = df.merge(bureau_agg, on = 'SK_ID_CURR', how = 'left')

    # Merge with the monthly information grouped by client
    df = df.merge(bureau_balance_by_client, on = 'SK_ID_CURR', how = 'left')
    
    
    return df.drop(columns = cols_to_remove)