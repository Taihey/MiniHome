from tkinter import *
from tkinter import ttk
from datetime import date, datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

root = Tk()
root.resizable(False, False)

scene = PhotoImage(file="./picture/screen.png").subsample(2, 2)
#ボタンの画像
btnImage = PhotoImage(file="./picture/screen.png").subsample(45, 200)
    
def create_gui1():
    root.title("データ入力")
    root.geometry('1200x1000')

    canvas = Canvas(root)
    canvas.pack(fill="both", ipadx=100, ipady=50)
    canvas.create_image(500, 500, image=scene)

    frame1 = ttk.Frame(canvas, borderwidth=2, relief='ridge')
    frame1.pack(fill='x', padx=10, pady=10)
    button1 = ttk.Button(frame1, text='終了', command=quit, image=btnImage, compound='center')
    button1.pack(side='right')
    #新しいGUIへの移動のコマンド--------------------------
    def move_to_food_adition():
        root.destroy()
        create_gui2()
    #----------------------------------------------------
    button1_2 = ttk.Button(frame1, text='食材の追加', command=move_to_food_adition)  #()をつけなければ無限ループしないらしい。
    button1_2.pack(side='left')
    #更新------------------------------------------------
    def renew_gui():
        root.destroy()
        create_gui1()
    #----------------------------------------------------
    button1_3 = ttk.Button(frame1, text='更新', command=renew_gui)
    button1_3.pack(side='right')

    labelframe2 = LabelFrame(canvas, height=160, borderwidth=2, relief='ridge', text='データ入力')
    labelframe2.pack(fill='x',side='top', padx=10, pady=10)
    label2 = ttk.Label(labelframe2, font=("",14), text='日付;')
    label2.place(x=0, y=0)
    entry2 = ttk.Entry(labelframe2, font=("",14), width=10)
    entry2.insert(0, date.today())       #初期値を設定
    entry2.place(x=60, y=0)
    label2_2 = ttk.Label(labelframe2, font=("",14), text='時刻;')
    label2_2.place(x=210, y=0)
    entry2_2 = ttk.Entry(labelframe2, font=("",14), width=2)
    entry2_2.insert(0, datetime.now().hour)
    entry2_2.place(x=270, y=0)
    label2_3 = ttk.Label(labelframe2, font=("",14), text=':')
    label2_3.place(x=300, y=0)
    entry2_3 = ttk.Entry(labelframe2, font=("",14), width=2)
    entry2_3.insert(0, datetime.now().minute)
    entry2_3.place(x=310, y=0)
    label2_4 = ttk.Label(labelframe2, font=("",14), text='食材;')
    label2_4.place(x=380, y=0)
    #conboboxの設定-----------------
    df_food_sub = pd.read_pickle('df_food_sub.pickle')
    food = [df_food_sub.iloc[r, 0] for r in range(len(df_food_sub.index))]
    df_food_sub.to_pickle('df_food_sub.pickle')
    var = StringVar()
    combobox2 = ttk.Combobox(labelframe2, state='readonly', textvariable=var, values=food, width=30, height=20)
    combobox2.place(x=440, y=0)
    def select_combo(event):             #コールバック関数、Eventオブジェクトを受け取る。
        print(combobox2.get())
    combobox2.bind('<<ComboboxSelected>>', select_combo)   #イベントと関数をバインド
    #-----------------------------
    label2_5 = ttk.Label(labelframe2, font=("",14), text='量;')
    label2_5.place(x=740, y=0)
    entry2_4 = ttk.Entry(labelframe2, font=("",14), width=4)
    entry2_4.place(x=780, y=0)
    #登録ボタンのコマンド--df_eat_testに入力を追加して、df_eatcalに自動追加-----------
    def add_data():
        try:
            df_food_sub = pd.read_pickle('df_food_sub.pickle')
            df_eat_sub = pd.read_pickle('df_eat_sub.pickle')
            df_eatcal_sub = pd.read_pickle('df_eatcal_sub.pickle')
            df_eat_sub.loc[len(df_eat_sub.index), :] = [                      #df_eat_testに追加
                entry2.get(), float(entry2_2.get()), float(entry2_3.get()), combobox2.get(), float(entry2_4.get())
            ]       #時間をfloatにしないと、グラフが表示されなかった。
            for x1 in range(len(df_food_sub.index)):                           #df_eatcal_testに自動追加
                if df_eat_sub.iloc[len(df_eat_sub) - 1, 3] == df_food_sub.iloc[x1, 0]:
                    df_eatcal_sub.loc[len(df_eat_sub) - 1, 'カロリー'] = round(df_food_sub.iloc[x1, 2]*(df_eat_sub.iloc[len(df_eat_sub) - 1, 4]/df_food_sub.iloc[x1, 1]), 1)
                    df_eatcal_sub.loc[len(df_eat_sub) - 1, 'タンパク質'] = round(df_food_sub.iloc[x1, 3]*(df_eat_sub.iloc[len(df_eat_sub) - 1, 4]/df_food_sub.iloc[x1, 1]),2)
                    df_eatcal_sub.loc[len(df_eat_sub) - 1, '脂質'] = round(df_food_sub.iloc[x1, 4]*(df_eat_sub.iloc[len(df_eat_sub) - 1, 4]/df_food_sub.iloc[x1, 1]), 2)
                    df_eatcal_sub.loc[len(df_eat_sub) - 1, '炭水化物'] = round(df_food_sub.iloc[x1, 5]*(df_eat_sub.iloc[len(df_eat_sub) - 1, 4]/df_food_sub.iloc[x1, 1]), 2)
                    df_eatcal_sub.loc[len(df_eat_sub) - 1, '食塩相当量'] = round(df_food_sub.iloc[x1, 6]*(df_eat_sub.iloc[len(df_eat_sub) - 1, 4]/df_food_sub.iloc[x1, 1]), 4)
        
                    break
                else:
                    pass
            #print(df_eatcal_sub)
            df_food_sub.to_pickle('df_food_sub.pickle')
            df_eat_sub.to_pickle('df_eat_sub.pickle')
            df_eatcal_sub.to_pickle('df_eatcal_sub.pickle')
            label2_6['text'] = str(combobox2.get()) + 'を追加しました。'
            entry2_4.delete(0, END)         #量の欄を削除して、連打防止。
        except:
            label2_6['text'] = '入力が完了していません。'
            print('入力が完了していません')
    #------------------------------------------------------------------------------
    button2 = ttk.Button(labelframe2, text='登録', width=5, command=add_data)
    button2.pack(side='right')
    label2_6 = ttk.Label(labelframe2, width=30)
    label2_6.place(x=850, y=0)

    #データを表示する場所を用意
    labelframe3 = LabelFrame(canvas, height=900, borderwidth=2, relief='ridge', text='データを表示')
    labelframe3.pack(fill='x', padx=10, pady=10)
    #treeviewのコラム
    column = ['日付', '時','分', '食品', '量', 'カロリー', 'タンパク質', '脂質', '炭水化物', '食塩相当量']
    tree3 = ttk.Treeview(labelframe3, columns=column, height=30)
    tree3.pack(side='left')
    #columnのフォーマットを定義
    tree3.column('#0', width=0, stretch='no'), tree3.heading('#0', text='Label')
    tree3.column('日付', width=120), tree3.heading('日付', text='日付')
    tree3.column('時', width=50), tree3.heading('時', text='時')
    tree3.column('分', width=50), tree3.heading('分', text='分')
    tree3.column('食品', width=220), tree3.heading('食品', text='食品')
    tree3.column('量', width=80), tree3.heading('量', text='量')
    tree3.column('カロリー', width=100), tree3.heading('カロリー', text='カロリー')
    tree3.column('タンパク質', width=100), tree3.heading('タンパク質', text='タンパク質')
    tree3.column('脂質', width=100), tree3.heading('脂質', text='脂質')
    tree3.column('炭水化物', width=100), tree3.heading('炭水化物', text='炭水化物')
    tree3.column('食塩相当量', width=100), tree3.heading('食塩相当量', text='食塩相当量')
    scrollbar3 = ttk.Scrollbar(labelframe3, orient=VERTICAL, command=tree3.yview)
    tree3["yscrollcommand"] = scrollbar3.set
    scrollbar3.pack(side='right')
    
    frame4 = ttk.Frame(canvas, height=30, borderwidth=2, relief='ridge')
    frame4.pack(fill='x', padx=10, pady=10)
    label3 = ttk.Label(frame4, font=("",14), text='日付を選択;')
    label3.place(x=0, y=0)
    #conboboxの設定---------------------------------------------------------------
    df_eat_sub = pd.read_pickle('df_eat_sub.pickle')
    dateselection = [df_eat_sub.iloc[r, 0] for r in range(len(df_eat_sub.index))]
    dateselection_kind = (np.array(list(set(dateselection))))
    dateitem = [i for i in dateselection_kind]
    df_eat_sub.to_pickle('df_eat_sub.pickle')
    #print(dateselection_kind)
    var = StringVar()
    combobox3 = ttk.Combobox(frame4, state='readonly', textvariable=var, values=dateitem, height=10)
    combobox3.place(x=130, y=0)
    #comboboxの関数、treeにデータを表示、合計値をlabelに表示、グラフも表示----------------------
    def select_combo(event):             
        #print(combobox3.get())
        for item in range(len(tree3.get_children())):  #要素を削除
            tree3.delete(item)
        
        df_eat_sub = pd.read_pickle('df_eat_sub.pickle')
        df_eatcal_sub = pd.read_pickle('df_eatcal_sub.pickle')
        df_eat_sub_day = df_eat_sub.loc[df_eat_sub.iloc[:, 0] == combobox3.get(), :]     #指定した日付のデータを抽出
        df_eatcal_sub_day = df_eatcal_sub.loc[df_eat_sub.iloc[:, 0] == combobox3.get(), :]
        
        #treeにデータを表示
        for i in range(len(df_eat_sub_day.index)):         
            combinedata = np.concatenate([
                [df_eat_sub_day.iloc[i, c1] for c1 in range(len(df_eat_sub_day.columns))],
                [df_eatcal_sub_day.iloc[i, c2] for c2 in range(len(df_eatcal_sub_day.columns))]
            ])
            combinedata_list = [item for item in combinedata]
            tree3.insert(parent='', index='end', iid=i, values=combinedata_list)
        
        #合計を計算
        calsum = df_eatcal_sub_day.sum(axis=0)
        #print(calsum)
        label3_2['text'] = (
            '合計:'+str(round(calsum[0], 1))+'kcal、タンパク質'+str(round(calsum[1], 1))+'g、脂質'+str(round(calsum[2], 1))+'g、炭水化物'+str(round(calsum[3], 1))+'g、食塩相当量'+str(round(calsum[4], 4))+'g'
            )
        
        df_eat_sub.to_pickle('df_eat_sub.pickle')
        df_eatcal_sub.to_pickle('df_eatcal_sub.pickle')
        #print(calsum)
        
        #グラフを表示
        x = np.arange(24)
        y_cal = [df_eatcal_sub_day.loc[df_eat_sub_day.loc[:, '時'] == h, 'カロリー'].sum(axis=0) for h in range(24)]
        y_pro = [df_eatcal_sub_day.loc[df_eat_sub_day.loc[:, '時'] == h, 'タンパク質'].sum(axis=0) for h in range(24)]
        y_fat = [df_eatcal_sub_day.loc[df_eat_sub_day.loc[:, '時'] == h, '脂質'].sum(axis=0) for h in range(24)]
        y_carb = [df_eatcal_sub_day.loc[df_eat_sub_day.loc[:, '時'] == h, '炭水化物'].sum(axis=0) for h in range(24)]
        y_solt = [df_eatcal_sub_day.loc[df_eat_sub_day.loc[:, '時'] == h, '食塩相当量'].sum(axis=0) for h in range(24)]
        fig, ax = plt.subplots(nrows=3)
        fig.suptitle('gain in ' + str(combobox3.get()))
        ax[0].bar(x, y_cal, label='calory')
        width=0.3
        x2 = [n - width for n in x]
        x3 = [n + width for n in x]
        ax[1].bar(x2, y_pro, width=width, label='protein', color='red')
        ax[1].bar(x, y_fat, width=width, label='fat', color='pink')
        ax[1].bar(x3, y_carb, width=width, label='carb', color='black')
        ax[2].bar(x, y_solt, label='solt', color='aqua')
        ax[0].set_xlabel('time')
        ax[0].set_ylabel('calory[cal]')
        ax[1].set_xlabel('time')
        ax[1].set_ylabel('weight[g]')
        ax[2].set_xlabel('time[hour]')
        ax[2].set_ylabel('weight[g]')
        ax[0].legend()
        ax[1].legend()
        ax[2].legend()
        ax[0].set_xticks(np.arange(24))
        ax[1].set_xticks(np.arange(24))
        ax[2].set_xticks(np.arange(24))
        plt.show()
    #------------------------------------------------------
    combobox3.bind('<<ComboboxSelected>>', select_combo)   #イベントと関数をバインド
    #-------------------------------------------------------------------------------------
    label3_2 = ttk.Label(frame4, font=("",14))
    label3_2.place(x=340, y=0)

    root.mainloop()

def create_gui2():
    #GUI作成--------------------------------------------
    root = Tk()
    root.title('layout2')
    root.geometry('1000x1000')

    frame1 = ttk.Frame(root, height=50, borderwidth=2, relief='ridge')
    frame1.pack(fill='x')
    button1 = ttk.Button(frame1, text='終了', command=quit)
    button1.pack(side='right')
    #guiの移動------------------------------
    def move_to_add_data():
        root.destroy()
        create_gui1()
    #---------------------------------------
    button1_2 = ttk.Button(frame1, text='データ入力へ', command=move_to_add_data)
    button1_2.pack(side='left')
    button3 = ttk.Button(frame1, text='データの編集')
    button3.pack(side='right')

    labelframe2 = LabelFrame(root, height=160, borderwidth=2, relief='ridge', text='食材の追加')
    labelframe2.pack(fill='x',side='top')
    label2 = ttk.Label(labelframe2, font=("",14), text='食材;')
    label2.place(x=0, y=0)
    entry2 = ttk.Entry(labelframe2, font=("",14), width=30)
    entry2.place(x=60, y=0)
    label2_2 = ttk.Label(labelframe2, font=("",14), text='量;')
    label2_2.place(x=500, y=0)
    entry2_2 = ttk.Entry(labelframe2, font=("",14), width=5)
    entry2_2.place(x=535, rely=0)
    label2_3 = ttk.Label(labelframe2, font=("",14), text='カロリー;')
    label2_3.place(x=0, y=50)
    entry2_3 = ttk.Entry(labelframe2, font=("",14), width=5)
    entry2_3.place(x=90, y=50)
    label2_4 = ttk.Label(labelframe2, font=("",14), text='タンパク質;')
    label2_4.place(x=180, y=50)
    entry2_4 = ttk.Entry(labelframe2, font=("",14), width=5)
    entry2_4.place(x=300, y=50)
    label2_5 = ttk.Label(labelframe2, font=("",14), text='脂質;')
    label2_5.place(x=380, y=50)
    entry2_5 = ttk.Entry(labelframe2, font=("",14), width=5)
    entry2_5.place(x=440, y=50)
    label2_6 = ttk.Label(labelframe2, font=("",14), text='炭水化物;')
    label2_6.place(x=550, y=50)
    entry2_6 = ttk.Entry(labelframe2, font=("",14), width=5)
    entry2_6.place(x=660, y=50)
    label2_7 = ttk.Label(labelframe2, font=("",14), text='食塩相当量;')
    label2_7.place(x=750, y=50)
    entry2_7 = ttk.Entry(labelframe2, font=("",14), width=5)
    entry2_7.place(x=880, y=50)
    #追加ボタンのコマンド----------------------------------
    def add_food():
        try:
            #DataFrameを用意------------------------
            df_food_sub = pd.read_pickle('df_food_sub.pickle')
            #---------------------------------------
            #入力が空だと、floatに変換できずにエラー
            additionaldata = [str(entry2.get()), float(entry2_2.get()), float(entry2_3.get()), float(entry2_4.get()), float(entry2_5.get()), float(entry2_6.get()), float(entry2_7.get())]
            df_food_sub.loc[len(df_food_sub.index), :] = additionaldata
            label2_8['text'] = str(entry2.get()) + 'を追加しました。'
            df_food_sub_sort = df_food_sub.sort_values('食材')          #食材を、あいうえお順に並べ替える。
            df_food_sub_sort2 = df_food_sub_sort.reset_index()          #バラバラになったindexを新しくふりなおす。
            df_food_sub_sort3 = df_food_sub_sort2.drop(columns='index') #古いindexを削除する。
            #print(df_food_sub)
            df_food_sub_sort3.to_pickle('df_food_sub.pickle')
            entry2.delete(0, END)     #ボタンを押したら、entryの中を消して、連打防止。
            entry2_2.delete(0, END)
        except:
            label2_8['text'] = '入力が完了していません'
    
    #-----------------------------------------------------
    button2 = ttk.Button(labelframe2, text='追加', command=add_food)
    button2.place(x=100, y=100)
    label2_8 = ttk.Label(labelframe2, font=("",14))
    label2_8.place(x=230, y=100)
    #表示ボタンのコマンド-----------------------------------
    def express_data():
        for item in range(len(tree3.get_children())):  #要素を削除
            tree3.delete(item)
        #tree3.delete(tree3.get_children()) #1次元のデータでないと削除できない
        
        df_food_sub = pd.read_pickle('df_food_sub.pickle')
        #print(df_food_sub)
        for i in range(len(df_food_sub.index)):         #treeにデータを表示
            tree3.insert(parent='', index='end', iid=i, values=[df_food_sub.iloc[i, c] for c in range(len(df_food_sub.columns))])
            #print(df_food_test.iloc[i, :])
        #print(tree3.get_children())
        df_food_sub.to_pickle('df_food_sub.pickle')
    #------------------------------------------------------
    button2_2 = ttk.Button(labelframe2, text='表示', command=express_data)
    button2_2.place(x=800, y=100)

    frame3 = ttk.Frame(root, borderwidth=2, relief='ridge')
    frame3.pack(fill='x')
    #treeviewのコラム
    column = ['食品', '量', 'カロリー', 'タンパク質', '脂質', '炭水化物', '食塩相当量']
    tree3 = ttk.Treeview(frame3, columns=column, height=20)
    tree3.pack(side='left')
    #columnのフォーマットを定義
    tree3.column('#0', width=0, stretch='no'), tree3.heading('#0', text='Label')
    tree3.column('食品', width=300), tree3.heading('食品', text='食品')
    tree3.column('量', width=100), tree3.heading('量', text='量')
    tree3.column('カロリー', width=100), tree3.heading('カロリー', text='カロリー')
    tree3.column('タンパク質', width=100), tree3.heading('タンパク質', text='タンパク質')
    tree3.column('脂質', width=100), tree3.heading('脂質', text='脂質')
    tree3.column('炭水化物', width=100), tree3.heading('炭水化物', text='炭水化物')
    tree3.column('食塩相当量', width=100), tree3.heading('食塩相当量', text='食塩相当量')
    scrollbar3 = ttk.Scrollbar(frame3, orient=VERTICAL, command=tree3.yview)
    tree3["yscrollcommand"] = scrollbar3.set
    scrollbar3.pack(side='right')


    root.mainloop()

create_gui2()