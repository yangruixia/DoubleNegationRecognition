import pandas as pd
import re
def index_check(Sent,S):
    token = Sent.group()
    df.at[index,'Token'] = token
    # Index部分
    fou1 = Sent.groups()[0] #第一个否定词
    fou2 = Sent.groups()[1] #第二个否定词
    if len(fou2)==2:
        fou1_index = '[(' + str(S.find(token)) + ',' + str(S.find(token)+len(fou1)) +')'
        fou2_index = ',(' + str(S.find(token)+len(token)-2) + ',' + str(S.find(token)+len(token)-1+len(fou2)-1) + ')]'
        Index = fou1_index+ fou2_index
        # print(S[S.find(token):S.find(token)+len(fou1)])
        # print(S[S.find(token)+len(token)-2:S.find(token)+len(token)-1+len(fou2)-1])
        # Check部分
        Check_sent = S[:S.find(token)] + '{' + fou1 + '}' + S[S.find(token)+len(fou1):S.find(token)+len(token)-len(fou2)] + '{' + fou2 + '}' + S[S.find(token)+len(token)-1+len(fou2)-1:]
    if len(fou2)==1:
        fou1_index = '[(' + str(S.find(token)) + ',' + str(S.find(token)+len(fou1)) +')'
        fou2_index = ',(' + str(S.find(token)+len(token)-1) + ',' + str(S.find(token)+len(token)-1+len(fou2)) + ')]'
        Index = fou1_index+ fou2_index
        # print(S[S.find(token):S.find(token)+len(fou1)])
        # print(S[S.find(token)+len(token)-1:S.find(token)+len(token)-1+len(fou2)])
            # Check部分
        Check_sent = S[:S.find(token)] + '{' + fou1 + '}' + S[S.find(token)+len(fou1):S.find(token)+len(token)-len(fou2)] + '{' + fou2 + '}' + S[S.find(token)+len(token)-1+len(fou2):]
    df.at[index,'Check'] = Check_sent
    return token,Index,Check_sent


def add_excel(df,lst):
    for ro in lst:
        index = ro[0]
        T = ro[1]
        S = ro[2]
        # 处理“类型”列
        pattern = r'“([^”]+)”'
        Type = re.findall(pattern, T)[0]

        # 处理“句子”列
        ## 1、并非不/没/没有/无、不无、没不、没有不、莫不、无不
        if Type in ['并非不/没/没有/无','不无','没不','没有不','莫不','无不']:
            Sent = re.compile(r'并非不|并非没有?|并非无|不无|没不|没有不|莫不|无不').search(S)
            if Sent:
                token = Sent.group()
                df.at[index,'Token'] = token
                # 处理Token
                start_index = S.find(token)
                end_index = start_index+len(token)
                df.at[index,'Index'] = f"[({start_index},{end_index})]"
                df.at[index,'Check'] = S[:start_index] + '{' + S[start_index:end_index] + '}' + S[end_index:]
                continue
            else:
                df.at[index,'Token'] = ''
        ## 2、不……不(不...不行/不好、不+非叙实动词+...不、不+非叙实动词+不、不+助动词+不、不+助动词+非叙实动词+...不、不+助动词+非叙实动词+不)
        elif Type in ['不+是+...不','不+助动词+非叙实动词+不','不...不行/不好','不+非叙实动词+...不','不+非叙实动词+不','不+助动词+不','不+助动词+非叙实动词+...不','不+助动词+非叙实动词+不']:
            Sent = re.compile(r'(不是?)[\u4e00-\u9fa5]+(不行?好?)').search(S)
            if Sent:
                token,Index,Check_sent = index_check(Sent,S)
                df.at[index,'Token'] = token
                df.at[index,'Index'] = Index
                df.at[index,'Check'] = Check_sent
                continue
            else:
                df.at[index,'Token'] = ''
                df.at[index,'Index'] = ''
                df.at[index,'Check'] = ''

        ## 3、不……没/没有(不+非叙实动词+没/没有、不+是+...没/没有、不+助动词+非叙实动词+...没/没有、不+助动词+非叙实动词+没/没有、不+助动词+没/没有)
        elif Type in ['不+非叙实动词+没/没有','不+是+...没/没有','不+助动词+非叙实动词+...没/没有','不+助动词+非叙实动词+没/没有','不+助动词+没/没有']:
            Sent = re.compile(r'(不是?)[\u4e00-\u9fa5]+(没有?)').search(S)
            if Sent:
                token,Index,Check_sent = index_check(Sent,S)
                df.at[index,'Token'] = token
                df.at[index,'Index'] = Index
                df.at[index,'Check'] = Check_sent
                continue
            else:
                df.at[index,'Token'] = ''
                df.at[index,'Index'] = ''
                df.at[index,'Check'] = ''
        ## 4、(非……莫属)
        elif Type in ['非...莫属']:
            Sent = re.compile(r'(非).+(莫属)').search(S)
            if Sent:
                token,Index,Check_sent = index_check(Sent,S)
                df.at[index,'Token'] = token
                df.at[index,'Index'] = Index
                df.at[index,'Check'] = Check_sent
                continue
            else:
                df.at[index,'Token'] = ''
                df.at[index,'Index'] = ''
                df.at[index,'Check'] = ''
        ### 5、(非...不/没/没有)
        elif Type == '非...不/没/没有':
            Sent = re.compile(r'(非).+(没有|没|不)').search(S)
            if Sent:
                token,Index,Check_sent = index_check(Sent,S)
                df.at[index,'Token'] = token
                df.at[index,'Index'] = Index
                df.at[index,'Check'] = Check_sent
                continue
            else:
                df.at[index,'Token'] = ''
                df.at[index,'Index'] = ''
                df.at[index,'Check'] = ''
        ## 6、(非...不可/不行)
        elif Type == '非...不可/不行':
            Sent = re.compile(r'(非).+(不可|不行)').search(S)
            if Sent:
                token,Index,Check_sent = index_check(Sent,S)
                df.at[index,'Token'] = token
                df.at[index,'Index'] = Index
                df.at[index,'Check'] = Check_sent
                continue
            else:
                df.at[index,'Token'] = ''
                df.at[index,'Index'] = ''
                df.at[index,'Check'] = ''

        ## 7、(绝非不/没/没有/无)
        elif Type in ['绝非不/没/没有/无']:
            Sent = re.compile(r'绝非不|绝非没|绝非没有|绝非无').search(S)
            if Sent:
                token = Sent.group()
                df.at[index,'Token'] = token
                start_index = S.find(token)
                end_index = start_index+len(token)
                df.at[index,'Index'] = f"[({start_index},{end_index})]"
                df.at[index,'Check'] = S[:start_index] + '{' + S[start_index:end_index] + '}' + S[end_index:]
                continue
            else:
                df.at[index,'Token'] = ''
        ## 8、(没/没有...不)
        elif Type in ['没/没有...不']:
            Sent = re.compile(r'(没有?).+(不)').search(S)
            if Sent:
                token,Index,Check_sent = index_check(Sent,S)
                df.at[index,'Token'] = token
                df.at[index,'Index'] = Index
                df.at[index,'Check'] = Check_sent
                continue
            else:
                df.at[index,'Token'] = ''
                df.at[index,'Index'] = ''
                df.at[index,'Check'] = ''
        ## 9、(无...不)
        elif Type in ['无...不']:
            # Sent = re.compile(r'(无).+(不)').search(S)
            # if Sent:
            #     token,Index,Check_sent = index_check(Sent,S)
            #     df.at[index,'Check'] = Check_sent
            #     continue
            # else:
            #     df.at[index,'Token'] = ''
            #     df.at[index,'Index'] = ''
            #     df.at[index,'Check'] = ''
            pp= r'(无)([\u4e00-\u9fa5]+)(不)'
            res=[]#存放标准形式的index
            token=''
            Index=''
            check=''
            all=[]#存放check里面需要标注的位置以及标注的符号
            for match in re.finditer(pp, S):
                t=[]#中间变量存放每一对双重否定词的index
                t.append((match.start(1), match.end(1)))
                t.append((match.start(3), match.end(3)))
                all.append((match.start(1),'{'))
                all.append((match.end(1),'}'))
                all.append((match.start(3),'{'))
                all.append((match.end(3),'}'))
                res.append(t)
            Index=",".join([str(sublist) for sublist in res])
            for i in res:
                for j in range(i[0][0],i[1][1]):
                    token+=str(S[j])
                if(i!=res[len(res)-1]):
                    token+=','
            #倒序地对该句进行标注        
            def insert_symbols(original_str, symbols_to_insert):
                for position, symbol in reversed(symbols_to_insert):
                    original_str = original_str[:position] + symbol + original_str[position:]
                return original_str
            check = insert_symbols(S, all)
                       
            df.at[index,'Token'] = token
            df.at[index,'Index'] = Index
            df.at[index,'Check'] = check
        ## 10、(没/没有...没/没有np)
        elif Type == '没/没有...没/没有np':
            Sent = re.compile(r'(没有?).+(没有?)').search(S)
            if Sent:
                token,Index,Check_sent = index_check(Sent,S)
                df.at[index,'Token'] = token
                df.at[index,'Index'] = Index
                df.at[index,'Check'] = Check_sent
                continue
            else:
                df.at[index,'Token'] = ''
                df.at[index,'Index'] = ''
                df.at[index,'Check'] = ''
        # 其他 
        else:
            df.at[index,'Token'] = ''
        if df.at[index,'Token'] == '':
            # 处理“句子”列
            ## 1、无一|莫非|无不|莫不|并非不|没|没有|无|别没|不无|绝非不|没不|没有不
            Sent = re.compile(r'无一|莫非|无不|莫不|并非不|别没|不无|绝非不|没不|没有不').search(S)
            if Sent:
                token = Sent.group()
                df.at[index,'Token'] = token
                start_index = S.find(token)
                end_index = start_index+len(token)
                df.at[index,'Index'] = f"[({start_index},{end_index})]"
                df.at[index,'Check'] = S[:start_index] + '{' + S[start_index:end_index] + '}' + S[end_index:]
                continue
            else:
                pass
            ## 2、不……不
            Sent = re.compile(r'(不是?|不可?|不得?)[\u4e00-\u9fa5]+(不)').search(S)
            if Sent:
                token,Index,Check_sent = index_check(Sent,S)
                df.at[index,'Token'] = token
                df.at[index,'Index'] = Index
                df.at[index,'Check'] = Check_sent
                continue
            else:
                pass
            ## 3、不……没/没有
            Sent = re.compile(r'(不是?)[\u4e00-\u9fa5]+(没有?)').search(S)
            if Sent:
                token,Index,Check_sent = index_check(Sent,S)
                df.at[index,'Token'] = token
                df.at[index,'Index'] = Index
                df.at[index,'Check'] = Check_sent
                continue
            else:
                pass
            ## 4、非……莫属
            Sent = re.compile(r'(非).+(莫属|不可?)').search(S)
            if Sent:
                token,Index,Check_sent = index_check(Sent,S)
                df.at[index,'Token'] = token
                df.at[index,'Index'] = Index
                df.at[index,'Check'] = Check_sent
                continue
            else:
                pass
            # # 5、非……不没／没有
            # Sent4 = re.compile(r'(非).+(不可?)').search(S)
            # if Sent4:
            #     token = Sent4.group()
            #     df.at[index,'Token'] = token
            #     start_index = S.find(token)
            #     end_index = start_index+len(token)
            #     df.at[index,'Index'] = f"({start_index},{end_index})"
            #     df.at[index,'Check'] = S[start_index:end_index]
            #     continue
            # else:
            #     pass

            ## 7、不+是+...不
            Sent = re.compile(r'(不是).+(不)').search(S)
            if Sent:
                token,Index,Check_sent = index_check(Sent,S)
                df.at[index,'Token'] = token
                df.at[index,'Index'] = Index
                df.at[index,'Check'] = Check_sent
                continue
            else:
                pass
            ## 6、非……不可／不行
            Sent = re.compile(r'(非).+(不可|不行)').search(S)
            if Sent:
                token,Index,Check_sent = index_check(Sent,S)
                df.at[index,'Token'] = token
                df.at[index,'Index'] = Index
                df.at[index,'Check'] = Check_sent
                continue
            else:
                pass


source_path = 'resource.xlsx'
df = pd.read_excel(source_path)

selected_columns = df.iloc[:, [0, 2]]

# 打印结果
sen_dic = []
# 得到类型和句子的字典      [index,Type列,Sentence列]
for index, row in df.iterrows():
    new_lst = [index,row['Type'],row['Sentence']]
    sen_dic.append(new_lst)

# print(sen_dic)
add_excel(df,sen_dic)
df.to_excel(source_path, index=False)