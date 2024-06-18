# imported modules


from tkinter.font import Font
import mysql.connector as msq
from tkinter.ttk import Combobox
import tkinter as tk
import os

# variables used

pas = 'tiger'
dbname = "stock_lkdjflsjkh"
existance = ''
list_100 = []

# predefined values
for i in range(101):
    list_100.append(i)


# Main Gui window
root = tk.Tk()
# root.geometry("800x800+300+90")
root.title("Medical Shop Manager")

font2 = Font(family='Lucida Bright', weight='bold')
font3 = Font(family='Lucida Bright', size=10)
font4= Font(family='Lucida Handwriting', weight='bold', size=16, underline=1)

# MySql connection handler

conet = msq.connect(host='localhost', user='root', passwd=pas)
cur = conet.cursor()
directory = os.environ.get('programdata')

# files used by the software

try:

    os.mkdir(directory + '\\Medicalshop')
    directory = directory + '\\Medicalshop'

except:
    directory = directory + '\\Medicalshop'

filetb = open('%s\\file_tb_bill.txt' % (directory), 'a+')
filemedi = open('%s\\file_medi.txt' % (directory), 'a+')


class medical_shop():

    def registering(self):

        a, b = self.new_u.get(), self.new_p.get()

        if a != '' and b != '':

            try:
                self.cursor.execute('INSERT INTO user_s(user_account,password) VALUES("%s","%s")' % (str(a), str(b)))
                conet.commit()
                self.frame2.destroy()
                self.login()

            except:
                self.frame2.destroy()
                self.register()

        else:
            self.frame2.destroy()
            self.register()

    def register(self):

        self.new_u = tk.StringVar()
        self.new_p = tk.StringVar()
        self.frame1.destroy()
        self.frame2 = tk.LabelFrame(self.master, text='Add New Account', padx=10, pady=10, font=font2)
        self.frame2.pack()
        label_user_r = tk.Label(self.frame2, text="User Name", font=font2).grid()
        in_user_r = tk.Entry(self.frame2, textvariable=self.new_u, font=font3).grid(row=0, column=1)
        label_pass_r = tk.Label(self.frame2, text="Password", font=font2).grid(row=1, column=0)
        in_pass_r = tk.Entry(self.frame2, textvariable=self.new_p, font=font3)
        in_pass_r.grid(row=1, column=1)
        button = tk.Button(self.frame2, text='Register', command=self.registering, font=font2)
        button.grid(row=2, column=0)
        button2 = tk.Button(self.frame2, text='Login', command=self.login_2, font=font2).grid(row=2, column=1)

    def login_2(self):

        self.frame2.destroy()
        self.login()

    def login(self):

        self.frame1 = tk.LabelFrame(self.master, text='Login into Your Account', padx=10, pady=10, font=font2)
        self.frame1.pack()
        self.label_user = tk.Label(self.frame1, text="User Name", font=font2).grid()
        self.in_user = tk.Entry(self.frame1, font=font3)
        self.in_user.grid(row=0, column=1)
        self.label_pass = tk.Label(self.frame1, text="Password", font=font2).grid(row=1)
        self.in_pass = tk.Entry(self.frame1, font=font3)
        self.in_pass.grid(row=1, column=1)
        self.button = tk.Button(self.frame1, text='Login', command=self.login_checker, font=font2)
        self.button.grid()
        self.button2 = tk.Button(self.frame1, text='Register', command=self.register, font=font2).grid(row=2, column=1)

    def login_checker(self):

        self.cursor.execute('select user_account, password from user_s')
        account = self.in_user.get()
        key = self.in_pass.get()
        list_got = (str(account), str(key))
        list_user = self.cursor.fetchall()

        for i in list_user:
            if i == list_got:
                self.permission = 'allowed'
                self.frame1.destroy()
                self.main_prog()
        self.cursor.reset()

    def add_medifile(self, medi_id, mname):

        list_medi = str(medi_id) + ' ' + (mname)
        self.file_medi.write(list_medi)
        self.file_medi.write('\n')
        self.file_medi.flush()

    def next_item(self):

        mname, qty, prz = self.name_var.get(), self.qty_var.get(), self.crt_price_var.get()
        self.medi_id += 1
        try:
            self.cursor.execute(
                'INSERT INTO Stock_av(Prod_id,Prod_name,Prod_av_qty,Prod_c_prz) VALUES("%s","%s","%s","%s")' % (
                self.medi_id, mname, qty, prz))
            conet.commit()
            self.add_medifile(self.medi_id, mname)
            self.frame_add_s.destroy()
            self.add_stock_entity()

            try:
                self.frame_crt_st.destroy()
                self.available_stock()
                self.frame_add_bill.destroy()
                self.generate_bill()

            except:
                self.available_stock()

        except:

            self.cursor.execute(
                'UPDATE Stock_av SET Prod_av_qty=Prod_av_qty+%s, Prod_c_prz=%s WHERE Prod_name= "%s"' % (
                qty, prz, mname))
            self.medi_id -= 1
            self.frame_add_s.destroy()
            self.add_stock_entity()

            try:
                self.frame_crt_st.destroy()
                self.available_stock()
                self.frame_add_bill.destroy()
                self.generate_bill()

            except:
                self.available_stock()

    def add_stock_entity(self):

        self.name_var = tk.StringVar()
        self.qty_var = tk.StringVar()
        self.crt_price_var = tk.StringVar()

        # font style

        font1 = Font(family='Lucida Bright', weight='bold')

        # stock adding frame
        self.frame_add_s = tk.LabelFrame(self.master, text='Enter The Stock Details', padx=10, pady=10, font=font1)
        self.frame_add_s.pack(side='left', fill='y')

        # Medicine name
        label_name = tk.Label(self.frame_add_s, text='Medecine Name', font=font1).grid(sticky="W")
        self.entry_name = tk.Entry(self.frame_add_s, textvariable=self.name_var, font=font3).grid(row=0, column=1)

        # medicine quantity
        label_qty = tk.Label(self.frame_add_s, text='Medicine Quantity', font=font1).grid(row=1, column=0, sticky="W")
        self.entry_qty = tk.Entry(self.frame_add_s, textvariable=self.qty_var, font=font3).grid(row=1, column=1)

        # medicine prize
        label_price = tk.Label(self.frame_add_s, text='Selling Price', font=font1).grid(row=2, column=0, sticky="W")
        self.entry_crt_prz = tk.Entry(self.frame_add_s, textvariable=self.crt_price_var, font=font3).grid(row=2,
                                                                                                          column=1)

        # next entity addition
        self.button_add_name = tk.Button(self.frame_add_s, text='Next Item', command=self.next_item, font=font1).grid(
            row=3,
            column=0, columnspan=2)

    def creating_bill(self, n):
        date = str(self.date_c[0][0].day) + str(self.date_c[0][0].month) + str(self.date_c[0][0].year) + str(n)

        try:

            self.cursor.execute(
                'CREATE TABLE %s_bill(Prod_id CHAR(20), Prod_name CHAR(20) UNIQUE NOT NULL, Prod_b_qty INT,Prod_c_prz FLOAT)' % (
                    date))

            self.add_curent_table_bill = date + '_bill'

#writing billing files
            st = self.add_curent_table_bill +'   ' + str(self.date_c[0][0].isoformat())
            self.file_tb_bill.write(st)
            self.file_tb_bill.write('\n')
            self.file_tb_bill.flush()

        except:

            n += 1
            self.creating_bill(n)

    def next_item_bill(self):
        name,qty = self.entry_name_b.get(),self.entry_qty_b.get()

#extrcting from dictionary

        id_ = self.dict_name_id[name]
        prz = self.dict_id_price[str(id_)]

#creating list of billing data


        list_d1 = [id_,name,qty,prz]
        self.list_bill_data.append(list_d1)
        self.frame_add_bill.destroy()
        self.generate_bill()


    def done_bill(self):

        name, qty = self.entry_name_b.get(), self.entry_qty_b.get()
        self.frame_add_bill.destroy()
        self.generate_bill()
        id_ = self.dict_name_id[name]
        prz = self.dict_id_price[str(id_)]

#creating list of billing data

        list_d1 = [id_, name, qty, prz]
        self.list_bill_data.append(list_d1)

        n=1
        self.creating_bill(n)
        for i in self.list_bill_data:
            [_id,name,qty,prz]=i
            x=self.dict_id_qty[_id]

            if str(x)>=str(qty):

                self.cursor.execute(
                    "INSERT INTO %s VALUES('%s','%s','%s','%s')" % (self.add_curent_table_bill, _id, name, qty, prz))
                conet.commit()
                self.cursor.execute('UPDATE Stock_av SET Prod_av_qty = Prod_av_qty - %s WHERE Prod_id = %s' %(qty,_id))
                conet.commit()




            else:

                qty = x
                self.cursor.execute(
                    'INSERT INTO %s VALUES("%s","%s","%s","%s")' % (self.add_curent_table_bill, _id, name, qty, prz))
                conet.commit()
                self.cursor.execute(
                    'UPDATE Stock_av SET Prod_av_qty = Prod_av_qty - %s WHERE Prod_id = %s' % (qty, _id))
                conet.commit()
        self.printing_bill()
        self.frame_add_bill.destroy()
        self.generate_bill()
        self.list_bill_data = []

    def printing_bill(self):

        frame11 = tk.Toplevel()
        frame11.title('Customer Bill')

        # font styles
        n=0
        xx = Font(family='Lucida Bright', size=12, weight='bold')
        x = Font(size=12)
        label = tk.Label(frame11, text='Medicine Id', font=xx).grid(row=n, column=0, sticky='W')
        label2 = tk.Label(frame11, text='Medicine Name', font=xx).grid(row=n, column=1, sticky='W')
        label3 = tk.Label(frame11, text='Quantity', font=xx).grid(row=n, column=2, sticky='W')
        label4 = tk.Label(frame11, text='Price per Quantity', font=xx).grid(row=n, column=3, sticky='W')
        label5 = tk.Label(frame11, text='Sum', font=xx).grid(row=n, column=4, sticky='W')

#fetching data from MySql

        self.cursor.execute('SELECT * FROM %s ORDER BY Prod_id' %(self.add_curent_table_bill))
        list_data_bil = self.cursor.fetchall()
        self.cursor.execute('SELECT Prod_b_qty * Prod_c_prz from %s ORDER BY Prod_id' %(self.add_curent_table_bill))
        list_prod_qty = self.cursor.fetchall()
        self.cursor.execute('SELECT sum(Prod_b_qty * Prod_c_prz) from %s' %(self.add_curent_table_bill))
        list_prod_total = self.cursor.fetchall()

        length=len(list_data_bil)

        for i in range(length):

            n+=1
            [pid,pn,pq,pp],[su]=list_data_bil[i],list_prod_qty[i]

            label='label1'+str(n)
            label2='label2'+str(n)
            label3='label3'+str(n)
            label4='label4'+str(n)
            label5='label5'+str(n)

            label = tk.Label(frame11, text=pid, font=x).grid(row=n, column=0, sticky='W')
            label2 = tk.Label(frame11, text=pn, font=x).grid(row=n, column=1, sticky='W')
            label3 = tk.Label(frame11, text=pq, font=x).grid(row=n, column=2, sticky='W')
            label4 = tk.Label(frame11, text=pp, font=x).grid(row=n, column=3, sticky='W')
            label5= tk.Label(frame11, text=pp, font=x).grid(row=n, column=4,sticky='W')
        labe_t= tk.Label(frame11, text='Total Amount', font=xx).grid(row=n+1, column=0,rowspan=2,sticky='W')
        labe_A= tk.Label(frame11, text=list_prod_total, font=xx).grid(row=n+1, column=2,rowspan=2,sticky='W')
        self.frame_crt_st.destroy()
        self.available_stock()


    def generate_bill(self):

# bill handling frame

        self.frame_add_bill = tk.LabelFrame(self.master, text='Generate Bill', font=font2, padx=10, pady=15)
        self.frame_add_bill.pack(fill='y')

# Medicine name

        self.entry_name_b = tk.Variable()
        label_name = tk.Label(self.frame_add_bill, text='Medicine name', font=font2).grid(sticky='w')
        entry_b_n = Combobox(self.frame_add_bill, values=self.list_medi_name,textvariable=self.entry_name_b, height=20).grid(row=0, column=1)

# Medicine qty

        self.entry_qty_b = tk.Variable()
        self.entry_qty_b.set(value='0')
        label_value = tk.Label(self.frame_add_bill, text='Medicine Quantity', font=font2).grid(row=1, column=0,sticky='w')
        entry_b_q = Combobox(self.frame_add_bill, values=list_100,textvariable=self.entry_qty_b, height=10).grid(row=1, column=1)

 # buttons

        button_done = tk.Button(self.frame_add_bill, text='Done', command=self.done_bill,font=font2).grid(row=2, column=0)
        button = tk.Button(self.frame_add_bill, text='Next Item', command=self.next_item_bill, font=font2).grid(row=2, column=1)

    def available_stock(self):

        # font styles
        xx = Font(family='Lucida Calligraphy', size=12, weight='bold')
        x = Font(size=12)

        self.frame_crt_st = tk.LabelFrame(self.master, text="Available Stock", padx=10, pady=10, font=xx)
        self.frame_crt_st.pack(side='right', fill='y')
        self.cursor.execute('SELECT * FROM Stock_av ORDER BY Prod_id')
        self.list_crt_stock = self.cursor.fetchall()
        n = 1

        # medicine scrollbar

        scroll_bar = tk.Scrollbar(self.frame_crt_st)
        scroll_bar.pack(side='right', fill='y')

        self.list_medi_name = []

        # list box for medicine name

        listbox = tk.Listbox(self.frame_crt_st, yscrollcommand=scroll_bar.set, font=x, width=40, height=40)
        listbox.pack(fill='y')
        a = 'Medicine Id' + ' Medicine Name' + ' Available Qty' + ' Selling Price'

        listbox.insert(1, a)

#variables for id and name

        self.dict_id_price = {}
        self.dict_name_id = {}
        self.dict_id_qty = {}

        for a in self.list_crt_stock:
            n += 1

# About medicines
            ava_len = [11, 15, 15, 15]
            [pid, pn, pq, pp, d] = a
            len_a = [7, len(str(pn)), len(str(pq)), len(str(pp))]
            list_in = [str(pid), str(pn), str(pq), str(pp)]
            list_out = ''

            n2 = 0

            for i in len_a:

                if i < ava_len[n2]:
                    x = ava_len[n2] - i
                    c = ' ' * x
                    new = list_in[n2] + c
                    list_out = list_out + new

                n2 += 1

            self.dict_id_price[str(pid)] = str(pp)
            self.dict_id_qty[str(pid)] = str(pq)
            self.list_medi_name.append(pn)
            listbox.insert(n, list_out)

        scroll_bar.config(command=listbox.yview)

#dictonary of names and id

        file1= open('%s\\file_medi.txt' % (directory), 'r')
        file_d = file1.readlines()
        n1 = len(file_d)

        for i in range(n1):
            x = file_d[i].split()
            self.dict_name_id[x[1]] = x[0]

        file1.close()

    def medi_id_fetch(self):
        self.cursor.execute('SELECT Prod_id FROM stock_av ORDER BY Prod_id')
        id_list = self.cursor.fetchall()
        length = len(id_list)

        if length != 0:

            last_id = id_list[length - 1]
            self.medi_id = int(last_id[0])

        else:
            self.medi_id = 1000000

    def __init__(self, master, cur, file_tb_bill, file_medi, directory):

        # class variables

        self.directory = directory
        self.file_tb_bill = file_tb_bill
        self.file_medi = file_medi
        self.permission = "none"
        self.master = master
        self.cursor = cur
        self.cursor.execute('select curdate()')
        self.date_c = self.cursor.fetchall()
        self.list_bill_data = []

        # initial processes
        self.medi_id_fetch()
        self.login()

    def main_prog(self):

        self.frame_main = tk.Frame(self.master)

        self.frame_main.pack(fill='x')
        button2 = tk.Label(self.frame_main, text='Medical Shop Management Software', font=font4,pady=15).pack()
        self.available_stock()
        self.add_stock_entity()
        self.generate_bill()


#cur.execute('drop database %s'%(dbname))
cur.execute('show databases')

for i in cur:
    if i[0] == dbname:
        existance = 'yes'

if existance != 'yes':
    cur.execute('CREATE DATABASE %s' % (dbname))
    cur.execute('use %s' % (dbname))
    cur.execute(
        "CREATE TABLE stock_av (Prod_id  INT PRIMARY KEY , Prod_name CHAR(20) UNIQUE NOT NULL, Prod_av_qty INT, Prod_c_prz FLOAT , last_update DATE)")
    cur.execute(
        "CREATE TABLE user_s (user_account CHAR(20) NOT NULL UNIQUE, password char(20) NOT NULL,date_of_creation DATE)")
    object = medical_shop(root, cur, filetb, filemedi, directory)

elif existance == 'yes':
    cur.execute('use %s' % (dbname))
    object = medical_shop(root, cur, filetb, filemedi, directory)

root.mainloop()
