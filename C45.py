import pandas as pd
import numpy as np
import sys

def entropiS(df_pred):
    count_label = pd.DataFrame(index=[1])
    total = 0

    for index in df_pred.index:
        total += 1
        if(df_pred[index] in count_label):
            count_label[df_pred[index]] +=1
        else:
            count_label[df_pred[index]] =1
    # print("count_label:")
    # print(count_label)
    # print()
    entropi_value =0
    for colomn in count_label:
        local_entropi = (-1)*(count_label[colomn]/total)*np.log2(count_label[colomn]/total)
        # print(colomn,":",local_entropi[1])
        entropi_value += local_entropi
    # print()
    # print('entropi :',entropi_value[1])
    # print()
    print(entropi_value)
    return entropi_value[1],count_label

def entropi(count,count_plus,count_min):
    if(count_plus != 0 and count_min!=0):
        return (-1)*(count_plus/count)*np.log2(count_plus/count) + (-1)*(count_min/count)*np.log2(count_min/count)
    else:
        return 0

def gain(df_attributes, df_prediction):
    entropi_value, count_label = entropiS(df_prediction)

    if(entropi_value == 0):
        return ['--',list(count_label.columns)[0]]
    # loop every colomns
    else:
        biggest_entropy = ['',0]
        for colomns in df_attributes:
            col_name = colomns
            # 2 as tepat waktu
            # 3 as Tidak tepat
            count = pd.DataFrame(index=[1,2,3])
            total = 0
            # index_target = pd.DataFrame({"name":[]})
            # print(index_target)

            # loop every value
            for index in df_attributes[colomns].index:
                total += 1
                if df_attributes[colomns][index] in count:
                    # count[df_attributes[colomns][i]][1] +=1
                    count.loc[1,df_attributes[colomns][index]] += 1
                    if df_prediction[index] == "tepat waktu":
                        count.loc[2, df_attributes[colomns][index]] += 1
                    else:
                        count.loc[3, df_attributes[colomns][index]] += 1
                else:
                    count.loc[1,df_attributes[colomns][index]]=1
                    if df_prediction[index] == "tepat waktu":
                        count.loc[2, df_attributes[colomns][index]] = 1
                        count.loc[3, df_attributes[colomns][index]] = 0
                    else:
                        count.loc[2, df_attributes[colomns][index]] = 0
                        count.loc[3, df_attributes[colomns][index]] = 1
            # print()
            # print(count)
            # print()

            # colomns of value
            tmp_entropi = entropi_value
            for colomns in count :
                tmp_entropi_eachValue = (count.loc[1,colomns]/total)*entropi(count.loc[1,colomns],count.loc[2,colomns],count.loc[3,colomns])
                # print(tmp_entropi_eachValue)
                tmp_entropi -= tmp_entropi_eachValue
            if biggest_entropy[1] < tmp_entropi:
                biggest_entropy[0] = col_name
                biggest_entropy[1] = tmp_entropi
            # print()
            # print("entropy",col_name,":",tmp_entropi)
            # print()
        return biggest_entropy


if __name__ == '__main__':
    id_target_iterasi = 0
    df_attributes = pd.read_excel("data.xlsx")
    df_prediction = df_attributes['ket']
    df_label = pd.DataFrame(index=df_attributes.index)
    df_label['label'] =0
    del df_attributes['ket']
    # print(df_attributes)
    # print(df_prediction)
    # print(df_label)
    # tree = pd.DataFrame({'id':[],'question':[],'option':[],'id_target':[]})
    tree = pd.DataFrame(columns=['question','option','id_target'])
    # max id_target
    id=0

    while(id_target_iterasi<=id):
        print("id_target",id_target_iterasi)
        print(df_label)
        df_prediction_now = df_prediction[df_label.label == id_target_iterasi]
        df_attributes_now = df_attributes[df_label.label == id_target_iterasi]
        gains = gain(df_attributes_now, df_prediction_now)
        col_name = gains[0]
        # print(col_name)
        value = gains[1]# yes no or value
        # print(value)

        if(col_name=='--'):
            tree = tree.append({'question':value,'option':'--','id_target':'--'},ignore_index=True)
            id_target_iterasi += 1
            # sys.exit()
        else:
            # labeling
            tmp_label_id = pd.DataFrame(columns=['label','id_target'])
            for i in df_attributes[col_name].index:
                if (tmp_label_id['label'].isin([df_attributes[col_name][i]]).any()):
                    for index in tmp_label_id['label'].index:
                        if(tmp_label_id['label'][index]==df_attributes[col_name][i] and df_label['label'][i]==id_target_iterasi):
                            df_label['label'][i] = tmp_label_id['id_target'][index]
                            break
                else:
                    if(df_label['label'][i]==id_target_iterasi):
                        id+=1
                        tmp_label_id = tmp_label_id.append({'label':df_attributes[col_name][i],'id_target':id},ignore_index=True)
                        df_label['label'][i] = id
            tree = tree.append({'question':col_name,'option':[tmp_label_id['label']],'id_target':[tmp_label_id['id_target']]},ignore_index=True)
            id_target_iterasi +=1
            # print(tree)
            # print(df_label)
            # print("id next:",id_target_iterasi)
            del df_attributes[col_name]
        print()
        print(tree)
        print()

