from typing import Union 
# Mengimpor modul Union dari pustaka typing untuk mendefinisikan hint tipe.
from fastapi import FastAPI
# Mengimpor kelas FastAPI dari pustaka fastapi.


app = FastAPI()
# Membuat instansi dari kelas FastAPI & menetapkannya ke variabel'app'.

#==================== FASTAPI GET ====================
@app.get("/") 
# Dekorator untuk menentukan titik akhir HTTP GET pada URL root ("/").
def read_root():# Definisi fungsi yang terkait dengan titik akhir root.
    return {"Hello": "World"}
# Mengembalikan respons JSON {"Hello": "World"} saat mengakses URL root.

@app.get("/mahasiswa/{nim}")
# Dekorator untuk menentukan titik akhir HTTP GET dengan parameter'nim'.
def ambil_mhs(nim:str): # Definisi fungsi, menerima parameter string 'nim'.
 return {"nama": "Budi Martami"}
# Mengembalikan respons JSON dengan nama "Budi Martami".

@app.get("/mahasiswa2/")
# Dekorator untuk menentukan titik akhir HTTP GET tanpa parameter jalur.
def ambil_mhs2(nim:str):# Definisi fungsi, menerima parameter string 'nim'.
 return {"nama": "Budi Martami 2"}
# Mengembalikan respons JSON dengan nama "Budi Martami 2".

@app.get("/daftar_mhs/") 
# Dekorator untuk menentukan titik akhir HTTP GET tanpa parameter jalur.
def daftar_mhs(id_prov:str,angkatan:str):
 # Definisi fungsi, menerima dua parameter string.
 return {"query":" idprov: {}  ; angkatan: {}".
 # Mengembalikan respons JSON dengan string query yang diformat.
 format (id_prov,angkatan),"data":[{"nim":"1234"},{"nim":"1235"}]}
# Mengembalikan daftar kamus yang berisi ID mahasiswa di bawah kunci 'nim'.

import sqlite3 # Mengimpor modul sqlite3 
@app.get("/init/")  
def init_db():
    try:
        DB_NAME = "upi.db" # Menetapkan nama file database.
        con = sqlite3.connect(DB_NAME) # Membuka koneksi ke database SQLite.
        cur = con.cursor() # Membuat objek cursor untuk mengeksekusi perintah SQL.
        
        # Perintah SQL untuk membuat tabel mahasiswa jika belum ada.
        create_table = """
        CREATE TABLE mahasiswa (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            nim TEXT NOT NULL,
            nama TEXT NOT NULL,
            id_prov TEXT NOT NULL,
            angkatan TEXT NOT NULL,
            tinggi_badan INTEGER
        )
        """
        cur.execute(create_table) # Menjalankan perintah SQL untuk membuat tabel.
        con.commit()  # Melakukan komit untuk menyimpan perubahan ke dalam database.           
    except: # Menangani pengecualian jika terjadi error.
        return {"status": "Terjadi error"}   
    finally: # Blok yang selalu dieksekusi, terlepas dari apakah terjadi pengecualian atau tidak.
        con.close()  # Menutup koneksi ke database.
    return {"status": "OK, database dan tabel berhasil dibuat"} # Mengembalikan pesan status berhasil.

from typing import Optional 
# Mengimpor modul Optional dari pustaka typing untuk mendefinisikan tipe opsional.
from fastapi import FastAPI, Response, Request 
# Mengimpor kelas FastAPI,Response,& Request dari pustaka FastAPI.
from pydantic import BaseModel
# Mengimpor kelas BaseModel dari modul pydantic untuk membuat model data.
class Mhs(BaseModel):# Mendefinisikan kelas Mhs yang mewarisi BaseModel.
 nim: str # Mendefinisikan atribut nim dengan tipe data string.
 nama: str # Mendefinisikan atribut nama dengan tipe data string.
 id_prov: str # Mendefinisikan atribut id_prov dengan tipe data string.
 angkatan: str # Mendefinisikan atribut angkatan dengan tipe data string.
 tinggi_badan: int | None = None
 # Mendefinisikan atribut tinggi_badan dengan tipe data integer/None sbg nilai default.



#==================== FASTAPI POST ====================
@app.post("/tambah_mhs/" , response_model=Mhs,status_code=201) 
# Dekorator untuk menentukan titik akhir HTTP POST pada URL /tambah_mhs/ 
# dengan mengatur model respons menjadi Mhs dan kode status respons menjadi 201.

def tambah_mhs(m:Mhs,response: Response, request: Request):
  # Definisi fungsi tambah_mhs yang menerima parameter m bertipe Mhs, 
  # dan parameter response serta request bertipe Response dan Request.
  try:
    DB_NAME = "upi.db"
    con = sqlite3.connect(DB_NAME) # Membuka koneksi ke database SQLite.
    cur = con.cursor()# Membuat objek cursor untuk mengeksekusi perintah SQL.
    # Eksekusi perintah SQL untuk menambahkan data mahasiswa ke tabel mahasiswa.
    cur.execute("""insert into mahasiswa (nim,nama,id_prov,angkatan,tinggi_badan) 
                  values 
    ( "{}","{}","{}","{}",{})""".format(m.nim,m.nama,m.id_prov,m.angkatan,m.tinggi_badan))
    con.commit() # Melakukan komit untuk menyimpan perubahan ke dalam database.
  except:
    return ({"status":"terjadi error"}) # Menangani pengecualian jika terjadi error.
  finally: 
    con.close() # Menutup koneksi ke database.
    response.headers["location"] = "/mahasiswa/{}".format(m.nim) #Menetapkan header lokasi respons.
    return m # Mengembalikan data mahasiswa yang baru ditambahkan.

# Menampilkan tampilan semua mahasiswa yang telah dipost
@app.get("/tampilkan_semua_mhs/")
def tampil_semua_mhs():
  try:
    DB_NAME = "upi.db"
    con = sqlite3.connect(DB_NAME) # Membuka koneksi ke database SQLite.
    cur = con.cursor() # Membuat objek cursor untuk mengeksekusi perintah SQL.
    recs = []
    # Mengambil semua data mahasiswa dari tabel mahasiswa.
    for row in cur.execute("select * from mahasiswa"):
        recs.append(row)
  except Exception as e:
    return  ({"status":"terjadi error"}) #Menangani pengecualian jika terjadi error.
  finally: 
    con.close() # Menutup koneksi ke database.
    return {"data":recs} # Mengembalikan data mahasiswa sebagai respons.



#==================== FASTAPI PUT ====================
from fastapi import FastAPI, Response, Request, HTTPException
# Mengimpor kelas FastAPI, Response, Request, dan HTTPException dari modul FastAPI.
import sqlite3 # Mengimpor modul sqlite3 untuk berinteraksi dengan database SQLite.

@app.put("/update_mhs_put/{nim}",response_model=Mhs)
# Dekorator untuk menentukan titik akhir HTTP PUT pada URL /update_mhs_put/{nim}, 
# dengan mengatur model respons menjadi Mhs.

def update_mhs_put(response: Response, nim: str, m: Mhs):
# Definisi fungsi update_mhs_put yang menerima parameter response,nim bertipe string,& m bertipe Mhs.
  try:
    DB_NAME = "upi.db" # Menetapkan nama file database.
    con = sqlite3.connect(DB_NAME) # Membuka koneksi ke database SQLite.
    cur = con.cursor()# Membuat objek cursor untuk mengeksekusi perintah SQL.
    
    # Mengambil data mahasiswa dari tabel mahasiswa berdasarkan NIM.
    cur.execute("select * from mahasiswa where nim = ?", (nim,) )
    existing_item = cur.fetchone() # Mengambil satu baris hasil dari eksekusi query.
  
  except Exception as e:  
    # Menangani pengecualian jika terjadi kesalahan dalam menjalankan query.
    raise HTTPException(status_code=500, detail="Terjadi exception:{}".format(str(e))) 
  if existing_item:# Jika item dengan NIM yang diberikan ditemukan dalam database.
        
    # Eksekusi query SQL untuk mengupdate data mahasiswa. 
    cur.execute("update mahasiswa set nama = ?, id_prov = ?, angkatan=?, tinggi_badan=? where nim=?", 
                (m.nama,m.id_prov,m.angkatan,m.tinggi_badan,nim))
    con.commit() # Melakukan komit untuk menyimpan perubahan ke dalam database.
    response.headers["location"] = "/mahasiswa/{}".format(m.nim)# Menetapkan header lokasi respons.

  else: 
        # Jika item dengan NIM yang diberikan tidak ditemukan dalam database.
        raise HTTPException(status_code=404, detail="Item Not Found")
 
  con.close() # Menutup koneksi ke database.
  return m  # Mengembalikan data mahasiswa yang telah diupdate.

#==================== FASTAPI PATCH ====================
class MhsPatch(BaseModel):
 nama: str | None = "kosong"
 # Mendefinisikan atribut nama dengan tipe data string opsional/None, dengan nilai default "kosong"
 id_prov: str | None = "kosong"
 # Mendefinisikan atribut id_prov dengan tipe data string opsional/None, dengan nilai default "kosong"
 angkatan: str | None = "kosong"
 # Mendefinisikan atribut angkatan dengan tipe data string opsional/None, dengan nilai default "kosong"
 tinggi_badan: Optional[int] | None = -9999
 # Mendefinisikan atribut tinggi_badan dengan tipe data integer opsional/None, dengan nilai default "null"

@app.patch("/update_mhs_patch/{nim}",response_model = MhsPatch)
def update_mhs_patch(response: Response, nim: str, m: MhsPatch ):
# Definisi fungsi update_mhs_patch yang menerima parameter response, nim bertipe string, dan m bertipe MhsPatch

  try:
    print(str(m))
    DB_NAME = "upi.db" # Menetapkan nama file database
    con = sqlite3.connect(DB_NAME) # Membuka koneksi ke database SQLite
    cur = con.cursor() # Membuat objek cursor untuk mengeksekusi perintah SQL
    
    # Mengambil data mahasiswa dari tabel mahasiswa berdasarkan NIM
    cur.execute("select * from mahasiswa where nim = ?", (nim,) ) 
    existing_item = cur.fetchone() # Mengambil satu baris hasil dari eksekusi query
  
  except Exception as e:
    # Menangani pengecualian jika terjadi kesalahan dalam menjalankan query
    raise HTTPException(status_code=500, detail="Terjadi exception: {}".format(str(e)))
 
  if existing_item:  # Jika item dengan NIM yang diberikan ditemukan dalam database
      sqlstr = "update mahasiswa set "# Membuat string query untuk mengupdate data mahasiswa 
  
      if m.nama!="kosong":# Jika nilai atribut nama dari objek m bukan "kosong"
          if m.nama!=None:# Jika nilai atribut nama dari objek m bukan None
              sqlstr = sqlstr + " nama = '{}' ,".format(m.nama)# Menambahkan string query untuk mengupdate atribut nama
          else: # Jika nilai atribut nama dari objek m adalah None
              sqlstr = sqlstr + " nama = null ," # Menambahkan string query untuk mengupdate atribut nama menjadi null
 
      if m.angkatan!="kosong":# Jika nilai atribut angkatan dari objek m bukan "kosong"
          if m.angkatan!=None:# Jika nilai atribut angkatan dari objek m bukan None
              sqlstr = sqlstr + " angkatan = '{}' ,".format(m.angkatan)# Menambahkan string query untuk mengupdate atribut angkatan
          else:# Jika nilai atribut angkatan dari objek m adalah None
              sqlstr = sqlstr + " angkatan = null ,"# Menambahkan string query untuk mengupdate atribut angkatan menjadi null

      if m.id_prov!="kosong":# Jika nilai atribut id_prov dari objek m bukan "kosong"
          if m.id_prov!=None:# Jika nilai atribut id_prov dari objek m bukan None
              sqlstr = sqlstr + " id_prov = '{}' ,".format(m.id_prov)# Menambahkan string query untuk mengupdate atribut id_prov
          else:# Jika nilai atribut id_prov dari objek m adalah None
              sqlstr = sqlstr + " id_prov = null, "# Menambahkan string query untuk mengupdate atribut id_prov menjadi null

      if m.tinggi_badan!=-9999: # Memeriksa apakah nilai tinggi_badan dari objek m bukan -9999
          if m.tinggi_badan!=None:# Memeriksa apakah nilai tinggi_badan dari objek m bukan None
              sqlstr = sqlstr + " tinggi_badan = {} ,".format(m.tinggi_badan)
              # Jika tidak None, tambahkan nilai tinggi_badan ke dalam string query
          else: # Jika nilai tinggi_badan dari objek m adalah None.
              sqlstr = sqlstr + " tinggi_badan = null ,"  # Jika None, set nilai tinggi_badan dalam database menjadi null      

      # Langkah serupa dilakukan untuk atribut angkatan, id_prov, dan tinggi_badan.
      sqlstr = sqlstr[:-1] + " where nim='{}' ".format(nim)# Menghapus koma terakhir dan menambahkan kondisi WHERE untuk NIM
      try:
          cur.execute(sqlstr)# Menjalankan query SQL untuk mengupdate data mahasiswa
          con.commit() # Melakukan komit untuk menyimpan perubahan ke dalam database
          response.headers["location"] = "/mahasixswa/{}".format(nim)# Menetapkan header lokasi respons

      except Exception as e:
          # Menangani pengecualian jika terjadi kesalahan dalam menjalankan query SQL
          raise HTTPException(status_code=500, detail="Terjadi exception: {}".format(str(e))) 
      
  else: # Jika item dengan NIM yang diberikan tidak ditemukan dalam database
    raise HTTPException(status_code=404, detail="Item Not Found")
 
  con.close() # Menutup koneksi ke database
  return m # Mengembalikan data mahasiswa yang telah diupdate
    

#==================== FASTAPI DELETE ====================
@app.delete("/delete_mhs/{nim}")
# Dekorator untuk menentukan titik akhir HTTP DELETE pada URL /delete_mhs/{nim}
def delete_mhs(nim: str):
    # Definisi fungsi delete_mhs yang menerima parameter nim bertipe string
    try:
        DB_NAME = "upi.db"# Menetapkan nama file database
        con = sqlite3.connect(DB_NAME) # Membuka koneksi ke database SQLite
        cur = con.cursor()  # Membuat objek cursor untuk mengeksekusi perintah SQL
        sqlstr = "delete from mahasiswa where nim='{}'".format(nim)
        # Membuat string query SQL untuk menghapus data mahasiswa berdasarkan NIM  
        print(sqlstr)  # Mencetak string query SQL (opsional)
        cur.execute(sqlstr)   # Menjalankan query SQL untuk menghapus data mahasiswa
        con.commit()  # Melakukan komit untuk menyimpan perubahan ke dalam database
    except:
        return {"status": "terjadi error"}  # Menangani pengecualian jika terjadi error
    finally:
        con.close() # Menutup koneksi ke database 
    return {"status": "ok"}  # Mengembalikan pesan status jika operasi berhasil


#==================== POST and GET file IMAGE ====================
from fastapi import File, UploadFile 
# Mengimpor fungsi File dan kelas UploadFile dari modul FastAPI
from fastapi.responses import FileResponse
# Mengimpor kelas FileResponse dari modul FastAPI untuk merespons file

@app.post("/uploadimage")
# Dekorator untuk menentukan titik akhir HTTP POST pada URL /uploadimage
def upload(file: UploadFile = File(...)):
    # Definisi fungsi upload yang menerima parameter file bertipe UploadFile
    try:
        print("Mulai upload")# Mencetak pesan awal upload
        print(file.filename) # Mencetak nama file yang diunggah
        contents = file.file.read() # Membaca konten dari file yang diunggah
        with open("./data_file/" + file.filename, 'wb') as f:
            f.write(contents)  # Menulis konten file ke dalam direktori data_file
    except Exception:
        return {"message": "Error upload file"} 
        # Menangani pengecualian jika terjadi error selama proses upload
        
    finally:
        file.file.close() # Menutup file yang diunggah setelah proses selesai 
    return {"message": "Upload berhasil: {}".format(file.filename)} 
    # Mengembalikan pesan berhasil jika proses upload selesai
    

# mengambil image berdasarkan nama file
@app.get("/getimage/{nama_file}")
# Dekorator untuk menentukan titik akhir HTTP GET pada URL /getimage/{nama_file}
async def getImage(nama_file: str):
# Definisi fungsi getImage yang menerima parameter nama_file bertipe string
    return FileResponse("./data_file/" + nama_file)  
    # Mengembalikan respons file gambar dengan nama yang sesuai dari direktori data_file

