# -*- coding:utf-8 -*-
from Tkinter import *
import sqlite3

class Main():
    def __init__(self, master):

        #frame
        frame=Frame(master, width=100,height=70)
        frame.pack()

        #label
        self.text=Label(frame, text="        ")
        self.text.pack()
        self.text.grid(row=0,sticky=W)
        self.text["text"]="               Adicionar Contato"

        #campos de texto
        self.lab=Label(frame, text="Nome")
        self.lab.pack(side=LEFT)
        self.lab.grid(row=1)

        self.name=Entry(frame, text="Nome", width=30)
        self.name.insert(0,"Digite o Nome")
        self.name.pack()
        self.name.grid(row=1)
        self.name.bind("<FocusIn>",self.clearName)

        self.phone=Entry(frame, text="Telefone",width=30)
        self.phone.insert(0,"Digite o Telefone")
        self.phone.pack()
        self.phone.grid(row=2)
        self.phone.bind("<FocusIn>",self.clearPhone)

        #botoes
        self.btn=Button(frame, text="Adicionar", command=self.adicionar)
        self.btn.pack()
        self.btn.grid(row=5,rowspan=1,sticky="w")

        self.attbtn=Button(frame, text="Editar", command=self.atualizar)
        self.attbtn.pack()
        self.attbtn.grid(row=5,rowspan=1,sticky="s")

        self.delbtn=Button(frame,text="Apagar",command=self.apagar)
        self.delbtn.pack()
        self.delbtn.grid(row=5,rowspan=1,sticky="e")
        
        #scrollbar
        scrollbar = Scrollbar(master)
        scrollbar.pack(side=RIGHT, fill=Y)

        #criando uma listbox
        self.content=Listbox(master,width=50)
        self.content.pack()
        #adicionando a scrollbar a listbox
        self.content.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.content.yview)

        #conexao com banco sqlite3
        self.conec=sqlite3.connect('contato.db')
        cur = self.conec.cursor()

        cur.execute("CREATE TABLE IF NOT EXISTS agenda("
                         "nome TEXT PRIMARY KEY NOT NULL,"
                         "telefone  TEXT NOT NULL)")
        self.conec.commit()
    
        #listando
        lista=cur.execute("SELECT * FROM agenda")
        self.conec.commit()
        for i in lista:
            self.content.insert(END,i)
        cur.close()
        
    #limpa o label do campo
    def clearName(self,event):
        self.name.delete(0,END)

    def clearPhone(self,event):
        self.phone.delete(0,END)

    #adiciona contato
    def adicionar(self):
        if self.name.get() =="":
            self.text["text"]="Preencha o campo"
        else:
            item1= self.name.get()
            item2=self.phone.get()

            self.name.delete(0,END)
            self.phone.delete(0,END)

            cur = self.conec.cursor()
            cur.execute("INSERT INTO agenda(nome,telefone) VALUES (?,?)",(item1,item2))
            self.conec.commit()
            cur.close()

            #insere no final da lista
            self.content.insert(END,(item1,item2))

    #apaga contato
    def apagar(self):
        #seleciona a linha
        contato = self.content.get(ACTIVE)
        namex = contato[0]

        cur=self.conec.cursor()
        cur.execute("DELETE FROM agenda WHERE nome=(?)",(namex,))
        self.conec.commit()
        cur.close()
        #deleta campo da lista
        self.content.delete(ANCHOR)

    #atualiza cotato, clica no campo e informa os valores como
    #se tivesse adicionando,alterações so estao aparecendo
    #apos fechar e abrir o programa
    def atualizar(self):
        contato=self.content.get(ACTIVE)
        namex=contato[0]

        item1= self.name.get()
        item2= self.phone.get()
        
        cur=self.conec.cursor()
        cur.execute("UPDATE agenda set nome =(?) , telefone=(?) WHERE nome=(?);",(item1,item2,namex))
        self.conec.commit()
        cur.close()
        self.content.update()


    def __del__(self):
        #fechar banco
        self.conec.close()

#inicia janela
app = Tk()
app.title("Minha Agenda")#titulo da janela
Main(app)
app.mainloop()
