import sqlite3 
import time

DEBUG = False #Activa/Desactiva prints de comprobacio 

#database = 'IS2017.db' #Nom de la base de dades que utilitzarem

class ISDB(object):
    
    database = 'IS2017.db' #Nom de la base de dades que utilitzarem   

    def ObtenirFoto(self,dni):
        """
        Retorna la ruta on es troba la foto del usuari {dni}

        @type dni: String
        @param dni: dni del usuari

        @type: List
        @return: llista amb la ruta de la foto
        """        
        sqlSentence = "SELECT Foto FROM tbl_Foto WHERE DNI = ?"
        conn = sqlite3.connect(self.database)
        c = conn.cursor()

        try:
            c.execute(sqlSentence,[dni])
            Data = c.fetchone()

            if DEBUG:
                for row in Data:
                    print(row)

            
        
        except sqlite3.Error as e:
            print("Error: ",e.args[0])

        conn.close()
        return Data[0]


    def ObtenirDadesPacient(self,dni):
        """
        Retorna una llista amb l'informacio del usuari {DNI,nom,cognoms,edat,enfermetat,habitacio asignada,
                                                        nom metge, cognom metge}

        @type dni: String
        @param dni: dni del usuari

        @type: List
        @return: llista de tuples amb l'informacio del pacient
        """        
        sqlSentence = """SELECT user.DNI,user.Nom,user.Cognoms,user.Edat,pac.Malaltia,pac.Habitacio,
                         (SELECT user.Nom FROM tbl_Usuari as user, tbl_Metge as met WHERE user.DNI =
                         (SELECT metpac.DNI_metge FROM tbl_MetgePacient as metpac WHERE metpac.DNI_usuari = ?)) as nom_metge,
                         (SELECT user.Cognoms FROM tbl_Usuari as user, tbl_Metge as met WHERE user.DNI =
                         (SELECT metpac.DNI_metge FROM tbl_MetgePacient as metpac WHERE metpac.DNI_usuari = ?)) as cognoms_metge
                         FROM tbl_Usuari as user,tbl_Pacient as pac, tbl_MetgePacient as metpac
                         Where user.DNI = ? and pac.DNI_usuari = ? and metpac.DNI_usuari = ?"""

        conn = sqlite3.connect(self.database)
        c = conn.cursor()        

        try:
            c.execute(sqlSentence,[dni,dni,dni,dni,dni])
            Data = c.fetchone()

            if DEBUG:
                for row in Data: #Printa el resultat de la query
                    print(row)
        except sqlite3.Error as e:
            print("Error: ",e.args[0])     
   
        conn.close()
        return Data

    def ObtenirNom(self,ID):
        """
        Retorna una llista amb la tupla del usuari que utilitza el XBEE {id}

        @type ID: String
        @param ID: El id del XBee en 16bits

        @type: List
        @return: llista amb la tupla DNI + nom + cognoms del usuari
        """
        sqlSentence = "SELECT user.DNI,user.Nom,user.Cognoms FROM tbl_Usuari as user, tbl_Pacient as pac WHERE pac.IDXBee = ? and user.DNI = pac.DNI_usuari"

        conn = sqlite3.connect(self.database)
        c = conn.cursor()

        try:            
            c.execute(sqlSentence,[ID])
            Data = c.fetchone()
            if DEBUG:
                for row in Data: #Printa el resultat de la query
                    print(row)          
        except sqlite3.Error as e:
            print("Error: ",e.args[0])   
     
        conn.close()

        if not Data: #Si no troba cap resultat
            Data = list()
        return Data

    def ObtenirID(self,dni):
        """
        Retorna una llista amb el ID del XBee que utilitza l'usuari {dni}

        @type dni: String
        @param nom: DNI del usuari
       
        @type: List        
        @return Data: llista amb la ID del XBee
        """
        sqlSentence = "SELECT pac.IDXBee FROM tbl_Pacient as pac, tbl_Usuari as user WHERE user.DNI = ? "

        conn = sqlite3.connect(self.database)
        c = conn.cursor()

        try:
            c.execute(sqlSentence,[dni])
            Data = c.fetchone()
            if DEBUG:
                for row in Data: #Printa el resultat de la query
                    print(row)
        except sqlite3.Error as e:
              print("Error: ",e.args[0])

        conn.close()
        return Data

    def ObtenirHabitacio(self,IDXBee):
        """
        Retorna una llista amb el numero de l'habitacio del XBee {IDXBee}

        @type dni: String
        @param nom: ID del XBee
       
        @type: List        
        @return Data: llista amb el numero d'habitacio
        """
        sqlSentence = "SELECT Ubicacio FROM tbl_XBee WHERE ID = ?"

        conn = sqlite3.connect(self.database)
        c = conn.cursor()

        try:
            c.execute(sqlSentence,[IDXBee])
            Data = c.fetchone()
            
            if DEBUG:
                for row in Data:
                    print(row)
        except sqlite3.Error as e:
            print("Error: ",e.args[0])

        conn.close()
        return Data[0]
            
                

    def ObternirListIDXBee(self):
        """
        Retorna una llista amb els IDs dels XBees que no estan assignats
        
        @type: List        
        @return Data: llistat amb la ID del XBee
        """
        sqlSentence = """SELECT xb.ID FROM tbl_XBee as xb WHERE xb.ID NOT IN (SELECT xb.ID FROM tbl_XBee as xb, tbl_Pacient as pac 
                         WHERE xb.ID = pac.IDXBee) and xb.Ubicacio = 'avi'"""

        conn = sqlite3.connect(self.database)
        c = conn.cursor()

        try:
            c.execute(sqlSentence)
            Data = c.fetchall()
            if DEBUG:
                for row in Data:                    
                    print(row[0])

            datalist = [i[0] for i in Data]

        except sqlite3.Error as e:
            print("Error: ",e.args[0])

        conn.close()

        if not Data: #Si no troba cap XBee disponible
            datalist = list()
        return datalist

    def ObtenirMetgeList(self):
        """
        Retorna una llista amb els DNIs dels metges
       
        @type: List        
        @return Data: llista amb els DNi
        """
        sqlSentence = "SELECT DNI FROM tbl_Metge"

        conn = sqlite3.connect(self.database)
        c = conn.cursor()

        try:
            c.execute(sqlSentence)
            Data = c.fetchall()
            if DEBUG:
                for row in Data:
                    print(row[0])    
            
            datalist = [i[0] for i in Data]

        except sqlite3.Error as e:
            print("Error: ",e.args[0])

        conn.close()   
        return datalist

    def AfegirXBee(self,idXBee,habitacio): 
        """
        Afegeix un XBee i l'usuari que l'utilitza a la base de dades

        @type idXBee: String
        @param idXBee: El id del XBee en 16bits        
        @type habitacio: String
        @param habitacio: numero de l'habitacio on es coloca el XBee
        
        @type: String        
        @return : String conforme s'ha afegit la relacio
        """
        sqlSentence = "INSERT INTO tbl_XBee VALUES(?,?)"        

        conn = sqlite3.connect(self.database)
        c = conn.cursor()

        try:
            c.execute(sqlSentence,[idXBee,habitacio])            
        except sqlite3.Error as e:
            print("Error: ", e.args[0])

        conn.commit()
        conn.close()

        return "Insertat"

    def AfegirMetge(self,dni,nom,cognoms,edat):
        """
        Afegeix un metge a la base de dades

        @type DNI: String
        @param DNI: DNI del metge
        @type nom: string
        @param nom: nom del metge
        @type cognoms: string
        @param cognoms: cognoms del metge
        
        @type: String        
        @return : String conforme s'ha afegit el metge
        """
        sqlSentence = "INSERT INTO tbl_Usuari VALUES(?,?,?,?)"
        sqlSentence2 = "INSERT INTO tbl_Metge VALUES(?)"

        conn = sqlite3.connect(self.database)
        c = conn.cursor()

        try:
            c.execute(sqlSentence,[dni,nom,cognoms,edat])
            c.execute(sqlSentence2,[dni])
        except sqlite3.Error as e:
            print("Error: ", e.args[0])

        conn.commit()
        conn.close()
    
        return "Insertat"
        

    def AfegirPacient(self,dni,nom,cognoms,habitacio,metge,malaltia,edat,IDXBee):
        """
        Afegeix un pacient a la base de dades

        @type DNI: String
        @param DNI: DNI del pacient
        @type nom: string
        @param nom: nom del pacient
        @type cognoms: string
        @param cognoms: cognoms del pacient
        @type habitacio: String
        @param habitacio: numero de l'habitacio assignada al pacient
        @type metge: String
        @param metge: DNI del metge assignat al pacient
        @type malaltia: string
        @param malaltia: nom de l'enfermetat del pacient si en te
        @type edat: String
        @param edat: edat del pacient
        @type IDXBee: String
        @param IDXBee: El id del XBee en 16bits

        @type: String        
        @return : String conforme s'ha afegit l'usuari
        """
        sqlSentence1 = "INSERT INTO tbl_Usuari VALUES(?,?,?,?)"
        sqlSentence2 = "INSERT INTO tbl_Pacient VALUES(?,?,?,?)"
        sqlSentence3 = "INSERT INTO tbl_MetgePacient VALUES(?,?)"

        conn = sqlite3.connect(self.database)
        c = conn.cursor()

        try:
            c.execute(sqlSentence1,[dni,nom,cognoms,edat])
            c.execute(sqlSentence2,[dni,IDXBee,malaltia,habitacio])
            c.execute(sqlSentence3,[metge,dni])
        except sqlite3.Error as e:
            print("Error: ", e.args[0])

        conn.commit()
        conn.close()
    
        return "Insertat"

    def AfegirFoto(self,dni,ruta):
        """
        Afegeix a la base de dades una ruta amb la foto {ruta} del usuari {dni}

        @type dni: String
        @param dni: dni del usuari
        @type ruta: String
        @param ruta: ruta de la foto    

        @type: String
        @return: String indicant la correcta inserció
        """        
        sqlSentence = "INSERT INTO tbl_Foto VALUES(?,?)"

        conn = sqlite3.connect(self.database)
        c = conn.cursor()

        try:
            c.execute(sqlSentence,[dni,ruta])
        except sqlite3.Error as e:
            print("Error: ", e.args[0])
    
        conn.commit()
        conn.close()

        return "Insertat"

    def EliminarPacient(self,dni):
        """
        Elimina el pacient amb dni {dni} de la base de dades

        @type dni: String
        @param dni: DNI del pacient a eliminar
                
        @type: String        
        @return : String conforme s'ha eliminat el pacient
        """
        sqlSentence = "DELETE FROM tbl_MetgePacient WHERE DNI_usuari = ?"
        sqlSentence2 = "DELETE FROM tbl_Pacient WHERE DNI_usuari = ?"
        sqlSentence3 = "DELETE FROM tbl_Foto WHERE DNI = ?"
        sqlSentence4 = "DELETE FROM tbl_Usuari WHERE DNI = ?"

        conn = sqlite3.connect(self.database)
        c = conn.cursor()

        try:
            c.execute(sqlSentence,[dni])
            c.execute(sqlSentence2,[dni])
            c.execute(sqlSentence3,[dni])
            c.execute(sqlSentence4,[dni])
        except sqlite3.Error as e:
            print("Error: ", e.args[0])

        conn.commit()
        conn.close()
        
        return "Eliminat"

    def EliminarXBee(self,ID):
        
        sqlSentence = "DELETE FROM tbl_XBee WHERE ID = ?"

        conn = sqlite3.connect(self.database)
        c = conn.cursor()

        try:
            c.execute(sqlSentence,[ID])
        except sqlite3.Error as e:
            print("Error: ", e.args[0])

        conn.commit()
        conn.close()

        return "Eliminat"                
    
    def EliminarMetge(self,dni):
        """
        Elimina el metge amb dni {dni} de la base de dades

        @type dni: String
        @param dni: DNI del metge a eliminar
                
        @type: String        
        @return : String conforme s'ha eliminat el metge
        """
        sqlSentence = "DELETE FROM tbl_MetgePacient WHERE DNI_metge = ?"
        sqlSentence2 = "DELETE FROM tbl_Metge WHERE DNI = ?"
        sqlSentence3 = "DELETE FROM tbl_Foto WHERE DNI = ?"
        sqlSentence4 = "DELETE FROM tbl_Usuari WHERE DNI = ?"

        conn = sqlite3.connect(self.database)
        c = conn.cursor()

        try:
            c.execute(sqlSentence,[dni])
            c.execute(sqlSentence2,[dni])
            c.execute(sqlSentence3,[dni])
            c.execute(sqlSentence4,[dni])
        except sqlite3.Error as e:
            print("Error: ", e.args[0])

        conn.commit()
        conn.close()
        
        return "Eliminat"

    def LogData(self,IDXBee,IDXBeeRoom):
        """
        Crea un log del XBee indicat {IDXBee} amb el nom de fitxer {IDXBee}

        @type IDXBee: String
        @param IDXBee: ID del XBee
        """        
        f = open('./'+ str(IDXBee)+ '.txt','a+') #Crea l'arxiu si no existeix i si existeix comenza a escriure a sota de l'ultima entrada
        dni = self.ObtenirNom(IDXBee)[0] #Agafem nomes el DNI del resultat
        habitacio = self.ObtenirHabitacio(IDXBeeRoom)
        
        hora = time.strftime("%H:%M:%S")
        dia =  time.strftime("%d/%m/%y")

        f.write("Dia: " + dia + '\n')
        f.write("Hora: " + hora + '\n')        
        f.write("Caiguda: " + habitacio + '\n')
       
        data = self.ObtenirDadesPacient(dni)             
        
        if DEBUG:
            for row in data:
                print(row)
        
        for i in data:
            f.write(str(i) + '\n')
            
        f.write('##############################' + '\n')

        f.close()


DB = ISDB() #Creem l'objecte de la base de dades
#cad = DB.ObtenirDadesPacient(1)
#print(cad)#Printem cada element de la tupla que retorna la funcio
#DB.ObtenirID(1)
#print(DB.ObtenirNom(234)[0]) #Printem l'usuari que porta el XBee [id]
#print(DB.AfegirXBee("5678","2FB2")) #Afegim un usuari amb el seu XBee (cap dels 2 existeix a la base de dades)
#DB.AfegirPacient(1234,"Pru","Eba",567,3,"",20,891)
#DB.EliminarUsuari(1)
#DB.LogData(852,234)
#cad = DB.ObternirListIDXBee()
#print(cad)
#print(DB.ObtenirMetgeList())
#DB.EliminarXBee(489)
#print(DB.ObtenirHabitacio(234))
#cad = DB.AfegirFoto(1234,"pc")
#print(cad)
#cad = DB.ObtenirFoto(1234)
#print(cad)
#DB.EliminarPacient(1234)