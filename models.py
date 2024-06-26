from sqlalchemy import Float, Table, Boolean, Column, Integer, String
from database import Base

class Kemiskinan(Base):
    __tablename__ = 'kemiskinan'

    id = Column(Integer, primary_key= True, index=True)
    kode_kabupaten_kota = Column(Integer)
    nama_kabupaten_kota = Column(String(250))
    jumlah_penduduk_miskin = Column(Float)
    satuan = Column(String(25))
    tahun = Column(Integer)
