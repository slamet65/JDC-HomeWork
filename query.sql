CREATE TABLE `kemiskinan` (
  `id` int NOT NULL,
  `kode_provinsi` int DEFAULT NULL,
  `nama_provinsi` varchar(250) DEFAULT NULL,
  `kode_kabupaten_kota` int DEFAULT NULL,
  `nama_kabupaten_kota` varchar(250) DEFAULT NULL,
  `jumlah_penduduk_miskin` double DEFAULT NULL,
  `satuan` varchar(25) DEFAULT NULL,
  `tahun` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
