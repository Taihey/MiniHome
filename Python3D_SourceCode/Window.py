from tkinter import *
from tkinter import ttk
from datetime import date, datetime
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

root = Tk()
root.geometry('1200x1000')
root.resizable(False, False)

scene = PhotoImage(file="./picture/screen.png").subsample(2, 2)
#ボタンの画像
btnImage = PhotoImage(file="./picture/screen.png").subsample(45, 200)

canvas = Canvas(root)
canvas.pack(fill="both", ipadx=10, ipady=10)
canvas.create_image(500, 500, image=scene)

class Window:
    def putDateCommbobox(self):
        #日付を選択
        self.selFrame = ttk.Frame(
            canvas, 
            height=30, borderwidth=2, relief='ridge',
            )
        self.selFrame.pack(fill='x', side='top', padx=10, pady=10)
        self.selLabel = ttk.Label(self.selFrame, font=("",14), text='日付を選択:')
        self.selLabel.place(x=0, y=0)
        
        var = StringVar()
        self.dateCombobox = ttk.Combobox(
            self.selFrame, 
            state='readonly', textvariable=var, height=10
            )
        self.dateCombobox.place(x=130, y=0)
        
    def putIndexCombobox(self):
        self.indFrame = ttk.Frame(
            canvas, 
            height=30, borderwidth=2, relief='ridge',
            )
        self.indFrame.pack(fill='x', side='top', padx=10, pady=10)
        self.indLabel = ttk.Label(self.indFrame, font=("",14), text='インデックスを選択:')
        self.indLabel.place(x=0, y=0)
        
        var = StringVar()
        self.indexCombobox = ttk.Combobox(
            self.indFrame, 
            state='readonly', textvariable=var, height=10
            )
        self.indexCombobox.place(x=200, y=0)
    
    def putRecordTree(self):
        #データを表示する場所を用意
        self.showFrame = ttk.Frame(
            canvas, 
            height=900, borderwidth=2, relief='ridge'
            )
        self.showFrame.pack(fill='x', padx=10, pady=10)
        #treeviewのコラム
        column = [
            'index', '日付', '時','分', '食品', '量', 
            'カロリー', 'タンパク質', '脂質', '炭水化物', '食塩相当量'
            ]
        width = [
            50, 120, 50, 50, 220, 80, 
            100, 100, 100, 100, 100
            ]
        self.showTree = ttk.Treeview(self.showFrame, columns=column, height=30)
        self.showTree.pack(side='left')
        #columnのフォーマットを定義
        self.showTree.column('#0', width=0, stretch='no')
        self.showTree.heading('#0', text='Label')
        for i in range(len(column)):
            self.showTree.column(column[i], width=width[i])
            self.showTree.heading(column[i], text=column[i])
        scrollbar = ttk.Scrollbar(
            self.showFrame, 
            orient=VERTICAL, command=self.showTree.yview
            )
        self.showTree["yscrollcommand"] = scrollbar.set
        scrollbar.pack(side='right')
    
    def putFoodTree(self):
        #データを表示する場所を用意
        self.showFoodFrame = ttk.Frame(
            canvas, 
            height=900, borderwidth=2, relief='ridge'
            )
        self.showFoodFrame.pack(fill='x', padx=10, pady=10)
        #treeviewのコラム
        column = [
            'index', '食品', '量', 'カロリー', 'タンパク質', '脂質', '炭水化物', '食塩相当量'
            ]
        width = [
            50, 300, 100, 100, 100, 100, 100, 100
            ]
        self.showFoodTree = ttk.Treeview(self.showFoodFrame, columns=column, height=30)
        self.showFoodTree.pack(side='left')
        #columnのフォーマットを定義
        self.showFoodTree.column('#0', width=0, stretch='no')
        self.showFoodTree.heading('#0', text='Label')
        for i in range(len(column)):
            self.showFoodTree.column(column[i], width=width[i])
            self.showFoodTree.heading(column[i], text=column[i])
        scrollbar = ttk.Scrollbar(
            self.showFoodFrame, 
            orient=VERTICAL, command=self.showFoodTree.yview
            )
        self.showFoodTree["yscrollcommand"] = scrollbar.set
        scrollbar.pack(side='right')
    
    #日付の配列を降順にソートする: yyyy-mm-ddの配列
    def sortDate(self, dates):
        def merge_sort(arr, start, end):
            if end-1 == start:
                return
            
            mid = int((start + end)/2)
            
            #一つになるまで分割する
            merge_sort(arr, start, mid)
            merge_sort(arr, mid, end)
            
            merge(arr, start, mid, end)
        
        #二つの配列を結合する 
        def merge(arr, start, mid, end):
            #分割
            nl = mid - start
            nr = end - mid
            left = []
            right = []
            for i in range(nl):
                left.append(arr[start + i])
            for i in range(nr):
                right.append(arr[mid + i])
            #マージ
            lIndex = 0
            rIndex = 0
            
            #yyyy -> mm -> dd の順に比べる
            #1つめの方が最近かどうか
            def compare(date1, date2): 
                dates1 = list(map(int, date1.split('-')))
                dates2 = list(map(int, date2.split('-')))
                for i in range(len(dates1)):
                    if dates1[0] > dates2[0]:
                        return True
                    elif dates1[0] < dates2[0]:
                        return False
                    elif dates1[0] == dates2[0]:
                        if dates1[1] > dates2[1]:
                            return True
                        elif dates1[1] < dates2[1]:
                            return False
                        elif dates1[1] == dates2[1]:
                            if dates1[2] > dates2[2]:
                                return True
                            else:
                                return False
            
            for i in range(start, end):
                if rIndex == nr:
                    arr[i] = left[lIndex]
                    lIndex += 1
                elif lIndex == nl:
                    arr[i] = right[rIndex]
                    rIndex += 1
                elif compare(left[lIndex], right[rIndex]):
                    arr[i] = left[lIndex]
                    lIndex += 1
                elif compare(left[lIndex], right[rIndex]) == False:
                    arr[i] = right[rIndex]
                    rIndex += 1
        
        merge_sort(dates, 0, len(dates))
        return dates
    
    def getFood(self):
        df_food = pd.read_pickle('df_food.pickle')
        food = [df_food.iloc[r, 0] for r in df_food.index]
        df_food.to_pickle('df_food.pickle')
        return food
    
    def createGUI(self):
        root.mainloop()
    
    #降順にソートした日付を返す
    def getDate(self):
        df_eat = pd.read_pickle('df_eat.pickle')
        date = [df_eat.iloc[r, 0] for r in range(len(df_eat.index))]
        dateSet = list(set(date))
        df_eat.to_pickle('df_eat.pickle')
        dates = self.sortDate(dateSet)
        return dates

class InputRecord(Window):
    def __init__(self):
        root.title("食事の記録")
        
        #終了ボタン
        self.menuFrame = ttk.Frame(canvas, borderwidth=2, relief='ridge')
        self.menuFrame.pack(side="top", pady=10)
        
        self.quitButton = ttk.Button(
            self.menuFrame, 
            text='終了', command=root.destroy, image=btnImage, compound='center'
        )
        self.quitButton.pack(side='right')
        
        #タイトル
        self.titleLabel = ttk.Label(canvas, text="食事の記録を入力してください", font=("",18))
        self.titleLabel.pack(side="top", pady=10)
        
        # 入力欄
        self.inputFrame = ttk.Frame(
            canvas, 
            height=30, borderwidth=2, relief='ridge',
            )
        self.inputFrame.pack(fill='x',side='top', padx=10, pady=10)
        
        self.dateLabel = ttk.Label(self.inputFrame, font=("",14), text='日付:')
        self.dateLabel.place(x=0, y=0)
        self.dateEntry = ttk.Entry(self.inputFrame, font=("",14), width=10)
        self.dateEntry.insert(0, date.today())       #初期値を設定
        self.dateEntry.place(x=60, y=0)
        
        self.timeLabel = ttk.Label(self.inputFrame, font=("",14), text='時刻:')
        self.timeLabel.place(x=210, y=0)
        self.hourEntry = ttk.Entry(self.inputFrame, font=("",14), width=2)
        self.hourEntry.insert(0, datetime.now().hour)
        self.hourEntry.place(x=270, y=0)
        self.sepLabel = ttk.Label(self.inputFrame, font=("",14), text=':')
        self.sepLabel.place(x=300, y=0)
        self.minEntry = ttk.Entry(self.inputFrame, font=("",14), width=2)
        self.minEntry.insert(0, datetime.now().minute)
        self.minEntry.place(x=310, y=0)
        
        self.foodLabel = ttk.Label(self.inputFrame, font=("",14), text='食材:')
        self.foodLabel.place(x=380, y=0)
        
        var = StringVar()
        self.foodCombobox = ttk.Combobox(
            self.inputFrame, 
            state='readonly', 
            textvariable=var,
            width=30, height=20
            )
        self.foodCombobox.place(x=440, y=0)
        
        self.amountLabel = ttk.Label(self.inputFrame, font=("",14), text='量:')
        self.amountLabel.place(x=740, y=0)
        self.amountEntry = ttk.Entry(self.inputFrame, font=("",14), width=4)
        self.amountEntry.place(x=780, y=0)
        
        self.addButton = ttk.Button(self.inputFrame, text='登録', width=5)
        self.addButton.pack(side='right')
        self.mesLabel = ttk.Label(self.inputFrame, width=30)
        self.mesLabel.place(x=850, y=0)
        
        #日付の選択のガイド
        self.titleLabel2 = ttk.Label(
            canvas, 
            text="記録を見たい日付を選択してください", font=("",18)
            )
        self.titleLabel2.pack(side="top", pady=10)
        
        #日付を選択
        self.putDateCommbobox()
        
        self.sumLabel = ttk.Label(self.selFrame, font=("",14))
        self.sumLabel.place(x=340, y=0)
        
        #treeを配置
        self.putRecordTree()
    
    #食事のデータを追加
    def addData(self): 
        try:
            df_food = pd.read_pickle('df_food.pickle')
            df_eat = pd.read_pickle('df_eat.pickle')
            df_eatcal = pd.read_pickle('df_eatcal.pickle')
            
            #摂取した食材とその時間、量を書き込む
            df_eat.loc[df_eat.index[-1] + 1, :] = [          
                self.dateEntry.get(), 
                int(self.hourEntry.get()), 
                int(self.minEntry.get()), 
                self.foodCombobox.get(), 
                float(self.amountEntry.get())
            ]       #時間をfloatにしないと、グラフが表示されなかった。
            
            #あらかじめ登録してある食材から、摂取したカロリーなどを計算し追加、
            for x1 in range(len(df_food.index)):                           
                if df_eat.loc[df_eat.index[-1], '食品'] == df_food.iloc[x1, 0]:
                    df_eatcal.loc[df_eat.index[-1], 'カロリー'] = round(
                        df_food.iloc[x1, 2]*
                        (df_eat.loc[df_eat.index[-1], "量(g, 合, 個)"]/df_food.iloc[x1, 1]), 
                        1
                    )
                    df_eatcal.loc[df_eat.index[-1], 'タンパク質'] = round(
                        df_food.iloc[x1, 3]*
                        (df_eat.loc[df_eat.index[-1], "量(g, 合, 個)"]/df_food.iloc[x1, 1]),
                        2
                    )
                    df_eatcal.loc[df_eat.index[-1], '脂質'] = round(
                        df_food.iloc[x1, 4]*
                        (df_eat.loc[df_eat.index[-1], "量(g, 合, 個)"]/df_food.iloc[x1, 1]), 
                        2
                    )
                    df_eatcal.loc[df_eat.index[-1], '炭水化物'] = round(
                        df_food.iloc[x1, 5]*
                        (df_eat.loc[df_eat.index[-1], "量(g, 合, 個)"]/df_food.iloc[x1, 1]), 
                        2
                    )
                    df_eatcal.loc[df_eat.index[-1], '食塩相当量'] = round(
                        df_food.iloc[x1, 6]*
                        (df_eat.loc[df_eat.index[-1], "量(g, 合, 個)"]/df_food.iloc[x1, 1]), 
                        4
                    )

                    break
            
            df_food.to_pickle('df_food.pickle')
            df_eat.to_pickle('df_eat.pickle')
            df_eatcal.to_pickle('df_eatcal.pickle')
            
            #日付の選択肢を追加
            self.dateCombobox["values"] = self.getDate()
            
            #treeを更新
            self.insertTree()
            
            self.mesLabel['text'] = str(self.foodCombobox.get()) + 'を追加しました。'
            self.amountEntry.delete(0, END)         #量の欄を削除して、連打防止。
            
            #表示しているデータを更新
            self.getDateSum()
            
        except:
            self.mesLabel['text'] = '入力が完了していません。'
            print('入力が完了していません')
    
    #指定した日付のデータを抜き出す
    def getDateData(self):
        df_eat = pd.read_pickle('df_eat.pickle')
        df_eatcal = pd.read_pickle('df_eatcal.pickle')
        #指定した日付のデータを抽出
        df_eat_day = df_eat.loc[
            df_eat.iloc[:, 0] == self.dateCombobox.get(), :
            ]     
        df_eatcal_day = df_eatcal.loc[
            df_eat.iloc[:, 0] == self.dateCombobox.get(), :
            ]
        df_eat.to_pickle('df_eat_sub.pickle')
        df_eatcal.to_pickle('df_eatcal_sub.pickle')
        
        return df_eat_day, df_eatcal_day
    
    #treeにデータを表示
    def insertTree(self):
        df_eat_day, df_eatcal_day = self.getDateData()
        
        #要素を削除
        for item in range(len(self.showTree.get_children())):  
            self.showTree.delete(item)
        
        for i in range(len(df_eat_day.index)):         
            combinedata = np.concatenate([
                df_eat_day.iloc[i, :], df_eatcal_day.iloc[i, :]
            ])
            
            #小数で保存した時間を整数として出力する
            combinedata[1] = int(combinedata[1])
            combinedata[2] = int(combinedata[2])
            combinedata = np.insert(combinedata, 0, df_eat_day.index[i])
            combinedata_list = [item for item in combinedata]
            self.showTree.insert(parent='', index='end', iid=i, values=combinedata_list)
        
    #指定した日付の合計を求める
    def getDateSum(self):
        df_eat_day, df_eatcal_day = self.getDateData()
        
        #合計を計算
        calsum = df_eatcal_day.sum(axis=0)
        self.sumLabel['text'] = (
            '合計:'+str(round(calsum[0], 1))+
            'kcal、タンパク質'+str(round(calsum[1], 1))+
            'g、脂質'+str(round(calsum[2], 1))+
            'g、炭水化物'+str(round(calsum[3], 1))+
            'g、食塩相当量'+str(round(calsum[4], 4))+'g'
            )
    
    #グラフを表示する
    def showGraph(self):
        df_eat_day, df_eatcal_day = self.getDateData()
        
        width=0.3
        x = np.arange(24)
        x2 = [n - width for n in x]
        x3 = [n + width for n in x]
        y_cal = [
            df_eatcal_day.loc[df_eat_day.loc[:, '時'] == h, 'カロリー'].sum(axis=0) 
            for h in range(24)
            ]
        y_pro = [
            df_eatcal_day.loc[df_eat_day.loc[:, '時'] == h, 'タンパク質'].sum(axis=0) 
            for h in range(24)
            ]
        y_fat = [
            df_eatcal_day.loc[df_eat_day.loc[:, '時'] == h, '脂質'].sum(axis=0) 
            for h in range(24)
            ]
        y_carb = [
            df_eatcal_day.loc[df_eat_day.loc[:, '時'] == h, '炭水化物'].sum(axis=0) 
            for h in range(24)
            ]
        y_solt = [
            df_eatcal_day.loc[df_eat_day.loc[:, '時'] == h, '食塩相当量'].sum(axis=0) 
            for h in range(24)
            ]
        fig, ax = plt.subplots(nrows=3)
        fig.suptitle('gain in ' + str(self.dateCombobox.get()))
        
        ax[0].bar(x, y_cal, label='calory')
        ax[1].bar(x2, y_pro, width=width, label='protein', color='red')
        ax[1].bar(x, y_fat, width=width, label='fat', color='pink')
        ax[1].bar(x3, y_carb, width=width, label='carb', color='black')
        ax[2].bar(x, y_solt, label='solt', color='aqua')
        
        ylabels = ['calory[cal]', 'weight[g]', 'weight[g]']
        for i in range(3):
            ax[i].set_ylabel(ylabels[i])
            ax[i].legend()
            ax[i].set_xticks(np.arange(24))
        ax[2].set_xlabel('time[hour]')
        plt.show()
        
    def selectDate(self, event):
        self.insertTree()
        self.getDateSum()
        self.showGraph()
        
    def createGUI(self):
        self.foodCombobox["values"] = self.getFood()
        
        self.dateCombobox["values"] = self.getDate()
        self.dateCombobox.bind('<<ComboboxSelected>>', self.selectDate)
        
        self.addButton["command"] = self.addData
        
        super().createGUI()

class EditRecord(InputRecord):
    def __init__(self):
        root.title("記録の編集")
        
        #終了ボタン
        self.menuFrame = ttk.Frame(canvas, borderwidth=2, relief='ridge')
        self.menuFrame.pack(side="top", pady=10)
        
        self.quitButton = ttk.Button(
            self.menuFrame, 
            text='終了', command=root.destroy, image=btnImage, compound='center'
            )
        self.quitButton.pack(side='right')
        
        #タイトル
        self.titleLabel = ttk.Label(
            canvas, 
            text="編集する記録の日付を選択してください", font=("",18)
            )
        self.titleLabel.pack(side="top", pady=10)
        
        #日付を選択
        self.putDateCommbobox()
        
        #treeを配置
        self.putRecordTree()
        
        self.selIndexLabel = ttk.Label(
            canvas, 
            text="削除するインデックスを選択してください", font=("",18)
            )
        self.selIndexLabel.pack(side="top", pady=10)
        
        #インデックスを選択
        self.putIndexCombobox()
        
        self.delButton = ttk.Button(self.indFrame, text='削除', width=5)
        self.delButton.pack(side='right')
        self.mesLabel = ttk.Label(self.indFrame, width=30)
        self.mesLabel.place(x=850, y=0)
    
    def editDate(self, event):
        self.insertTree()
        
        df_eat_day, df_eatcal_day = self.getDateData()
        index = df_eat_day.index
        #np.array -> list
        index = [idx for idx in index]
        self.indexCombobox["value"] = index
    
    def deleteIndex(self):
        df_eat = pd.read_pickle('df_eat.pickle')
        df_eatcal = pd.read_pickle('df_eatcal.pickle')
        
        #指定したインデックス番号の行を削除
        try:
            df_eat = df_eat.drop(index = int(self.indexCombobox.get()))
            df_eatcal = df_eatcal.drop(index = int(self.indexCombobox.get()))
            df_eat.to_pickle('df_eat.pickle')
            df_eatcal.to_pickle('df_eatcal.pickle')
            
            #コンボボックスの中身と、treeの中身を更新
            self.editDate(None)
            self.dateCombobox["values"] = self.getDate()
            
            self.mesLabel["text"] = (
                "インデックス" + str(self.indexCombobox.get()) + "を削除しました。"
                )
            
        except:
            self.mesLabel["text"] = "インデックス番号を選択してください"
            print("except")
            print(self.indexCombobox.get())
    
    def createGUI(self):
        self.dateCombobox["values"] = self.getDate()
        self.dateCombobox.bind('<<ComboboxSelected>>', self.editDate)
        
        self.delButton["command"] = self.deleteIndex
        
        root.mainloop()

class InputFood(Window):
    def __init__(self):
        root.title("食材の追加")
        
        #終了ボタン
        self.menuFrame = ttk.Frame(canvas, borderwidth=2, relief='ridge')
        self.menuFrame.pack(side="top", pady=10)
        
        self.quitButton = ttk.Button(
            self.menuFrame, 
            text='終了', command=root.destroy, image=btnImage, compound='center'
        )
        self.quitButton.pack(side='right')
        
        #タイトル
        self.titleLabel = ttk.Label(
            canvas, 
            text="追加する食材を入力してください", font=("",18)
            )
        self.titleLabel.pack(side="top", pady=10)
        
        #入力欄
        self.foodFrame = ttk.Frame(canvas, height=160, borderwidth=2, relief='ridge')
        self.foodFrame.pack(fill='x',side='top')
        self.gredLabel = ttk.Label(self.foodFrame, font=("",14), text='食材:')
        self.gredLabel.place(x=0, y=0)
        self.gredEntry = ttk.Entry(self.foodFrame, font=("",14), width=30)
        self.gredEntry.place(x=60, y=0)
        self.amountLabel = ttk.Label(self.foodFrame, font=("",14), text='量:')
        self.amountLabel.place(x=500, y=0)
        self.amountEntry = ttk.Entry(self.foodFrame, font=("",14), width=5)
        self.amountEntry.place(x=535, rely=0)
        self.calLabel = ttk.Label(self.foodFrame, font=("",14), text='カロリー:')
        self.calLabel.place(x=0, y=50)
        self.calEntry = ttk.Entry(self.foodFrame, font=("",14), width=5)
        self.calEntry.place(x=90, y=50)
        self.proLabel = ttk.Label(self.foodFrame, font=("",14), text='タンパク質:')
        self.proLabel.place(x=180, y=50)
        self.proEntry = ttk.Entry(self.foodFrame, font=("",14), width=5)
        self.proEntry.place(x=300, y=50)
        self.fatLabel = ttk.Label(self.foodFrame, font=("",14), text='脂質:')
        self.fatLabel.place(x=380, y=50)
        self.fatEntry = ttk.Entry(self.foodFrame, font=("",14), width=5)
        self.fatEntry.place(x=440, y=50)
        self.carbLabel = ttk.Label(self.foodFrame, font=("",14), text='炭水化物:')
        self.carbLabel.place(x=550, y=50)
        self.carbEntry = ttk.Entry(self.foodFrame, font=("",14), width=5)
        self.carbEntry.place(x=660, y=50)
        self.soltLabel = ttk.Label(self.foodFrame, font=("",14), text='食塩相当量:')
        self.soltLabel.place(x=750, y=50)
        self.soltEntry = ttk.Entry(self.foodFrame, font=("",14), width=5)
        self.soltEntry.place(x=880, y=50)
        
        self.foodAddButton = ttk.Button(self.foodFrame, text='追加')
        self.foodAddButton.place(x=400, y=100)
        self.addLabel = ttk.Label(self.foodFrame, font=("",14))
        self.addLabel.place(x=530, y=100)
        
        self.putFoodTree()
    
    #treeにデータを表示
    def insertFoodTree(self):
        #要素を削除
        for item in range(len(self.showFoodTree.get_children())):  
            self.showFoodTree.delete(item)
        
        df_food = pd.read_pickle('df_food.pickle')
        df_food_sort = df_food.sort_values('食材')
        
        for i in range(len(df_food.index)):         
            vals = df_food_sort.iloc[i, :]
            
            #index番号を追加
            vals = np.insert(np.array(vals), 0, df_food_sort.index[i])  
            val_list = [val for val in vals]
            self.showFoodTree.insert(
                parent='', index='end', iid=i, 
                values=val_list
                )
            
        df_food.to_pickle('df_food_sub.pickle')
        
    #新しい食材の追加
    def addFood(self):
        try:
            df_food = pd.read_pickle('df_food.pickle')
            #入力が空だと、floatに変換できずにエラー
            additionaldata = [
                str(self.gredEntry.get()), float(self.amountEntry.get()), 
                float(self.calEntry.get()), float(self.proEntry.get()), 
                float(self.fatEntry.get()), float(self.carbEntry.get()), 
                float(self.soltEntry.get())
                ]
            df_food.loc[df_food.index[-1] + 1, :] = additionaldata
            self.addLabel['text'] = str(self.gredEntry.get()) + 'を追加しました。'
            df_food.to_pickle('df_food.pickle')
            
            #ボタンを押したら、entryの中を消して、連打防止。
            self.gredEntry.delete(0, END)     
            self.amountEntry.delete(0, END)
            
            self.insertFoodTree()
            
        except:
            self.addLabel['text'] = '入力が完了していません'
        
    def createGUI(self):
        self.foodAddButton['command'] = self.addFood
        self.insertFoodTree()
        root.mainloop()

class EditFood(InputFood):
    def __init__(self):
        root.title("食材の編集")
        
        #終了ボタン
        self.menuFrame = ttk.Frame(canvas, borderwidth=2, relief='ridge')
        self.menuFrame.pack(side="top", pady=10)
        
        self.quitButton = ttk.Button(
            self.menuFrame, 
            text='終了', command=root.destroy, image=btnImage, compound='center'
        )
        self.quitButton.pack(side='right')
        
        #タイトル
        self.titleLabel = ttk.Label(
            canvas, 
            text="食材の一覧", font=("",18)
            )
        self.titleLabel.pack(side="top", pady=10)
        
        #treeの配置
        self.putFoodTree()
        
        self.subTitleLabel = ttk.Label(
            canvas, 
            text="削除する食材のindexを選択してください", font=("",18)
            )
        self.subTitleLabel.pack(side="top", pady=10)
        
        #インデックスを選択
        self.putIndexCombobox()
        self.delButton = ttk.Button(self.indFrame, text='削除', width=5)
        self.delButton.pack(side='right')
        self.mesLabel = ttk.Label(self.indFrame, width=30)
        self.mesLabel.place(x=850, y=0)
    
    def deleteIndex(self):
        df_food = pd.read_pickle('df_food.pickle')
        
        #指定したインデックス番号の行を削除
        try:
            df_food = df_food.drop(index = int(self.indexCombobox.get()))
            df_food.to_pickle('df_food.pickle')
            
            #コンボボックスの中身と、treeの中身を更新
            self.insertFoodTree()
            index = [ind for ind in df_food.index]
            self.indexCombobox["values"] = index
            
            self.mesLabel["text"] = (
                "インデックス" + str(self.indexCombobox.get()) + "を削除しました。"
                )
            
        except:
            self.mesLabel["text"] = "インデックス番号を選択してください"
            print("except")
            print(self.indexCombobox.get())
    
    def createGUI(self):
        self.insertFoodTree()
        
        df_food = pd.read_pickle('df_food.pickle')
        df_food.to_pickle('df_food.pickle')
        index = df_food.index
        index = [ind for ind in index]
        
        self.indexCombobox['values'] = index
        
        self.delButton['command'] = self.deleteIndex
        
        root.mainloop()

EditFood().createGUI()