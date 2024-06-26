from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import APIKeyHeader
from pydantic import BaseModel
from typing import Annotated
import models
from database import engine, Sessionlocal
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

load_dotenv()


app = FastAPI()
# models.Base.metadata.create_all(bind=engine)
models.Base.metadata.create_all(bind = engine)

def get_db():
    db = Sessionlocal()
    try: 
        yield db

    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

header_scheme = APIKeyHeader(name="x-key")

def sort_by_jml(e):
  return e.jumlah_penduduk_miskin

def sort_by_tahun(e):
  return e.tahun

def sort_by_pertumbuhan(e):
  return e["pertumbuhan"]

@app.get("/kemiskinan/kabkot/{tahun}", status_code= status.HTTP_200_OK)
async def read_kemiskinan(tahun: int, db: db_dependency):
    raw_data = db.query(models.Kemiskinan).filter(models.Kemiskinan.tahun == tahun).all()
    if len(raw_data) < 1:
        raise HTTPException(status_code=400, detail='Data Kemiskinan tidak ditemukan')
    raw_data.sort(key=sort_by_jml)
    data = {
        "data" : { }
    }

    for r in raw_data:
        data["data"][r.nama_kabupaten_kota] = r.jumlah_penduduk_miskin

    return data

@app.get("/kemiskinan/tahunan/{kode_wil}", status_code= status.HTTP_200_OK)
async def read_kemiskinan(kode_wil: int, db: db_dependency, key: str = Depends(header_scheme)):
    api_key = os.getenv("API_KEY")
    if key != api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    raw_data = db.query(models.Kemiskinan).filter(models.Kemiskinan.kode_kabupaten_kota == kode_wil).all()
    if len(raw_data) < 1:
        raise HTTPException(status_code=400, detail='Data wilayah tidak ditemukan')
    raw_data.sort(key=sort_by_tahun)
    data = {
        "data" : { }
    }
    for r in raw_data:
        data["data"][r.tahun] = r.jumlah_penduduk_miskin
    return data

@app.get("/kemiskinan/pertumbuhan/{ke}/{dari}", status_code= status.HTTP_200_OK)
async def read_kemiskinan(ke: int, dari:int, db: db_dependency, key: str = Depends(header_scheme)):
    api_key = os.getenv("API_KEY")
    if key != api_key:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    data_ke = db.query(models.Kemiskinan).filter(models.Kemiskinan.tahun == ke).all()
    data_dari = db.query(models.Kemiskinan).filter(models.Kemiskinan.tahun == dari).all()

    raw_data = []
    data = {
        "data" : { }
    }
    for r in data_ke:
        sebelum = next(x for x in data_dari if x.kode_kabupaten_kota == r.kode_kabupaten_kota)
        pertumbuhan = round(r.jumlah_penduduk_miskin - sebelum.jumlah_penduduk_miskin, 3)
        new_data = {
            "nama_kabupaten_kota" : r.nama_kabupaten_kota,
            "pertumbuhan" : pertumbuhan
        }
        raw_data.append(new_data)
    
    raw_data.sort(key=sort_by_pertumbuhan)

    for d in raw_data:
        data["data"][d["nama_kabupaten_kota"]] = d["pertumbuhan"]

    return data
