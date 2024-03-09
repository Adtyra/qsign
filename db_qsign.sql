-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 12, 2024 at 03:05 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_qsign`
--

-- --------------------------------------------------------

--
-- Table structure for table `tb_dk`
--

CREATE TABLE `tb_dk` (
  `id_k` int(11) NOT NULL,
  `nama` varchar(255) NOT NULL,
  `k_publik` varchar(255) NOT NULL,
  `id_p` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tb_pengguna`
--

CREATE TABLE `tb_pengguna` (
  `id_p` int(11) NOT NULL,
  `email` varchar(64) NOT NULL,
  `nama` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `foto` text NOT NULL,
  `bio` text DEFAULT NULL,
  `kunci_privat` text DEFAULT NULL,
  `kunci_publik` text DEFAULT NULL,
  `hidemail` int(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tb_pengguna`
--

INSERT INTO `tb_pengguna` (`id_p`, `email`, `nama`, `password`, `foto`, `bio`, `kunci_privat`, `kunci_publik`, `hidemail`) VALUES
(815861764, 'astra@gmail.com', 'astra', 'pbkdf2:sha256:260000$bnl9JeAq1fEyXPNI$2cf802970270e8db983465a192bffff6b3ffc9b2d9c2e28c14f41dfea10a75f2', 'default.png', 'Pemilik akun belum menulis bio', '-----BEGIN EC PRIVATE KEY-----\nMHcCAQEEIBNUXZbcgr+UqFbaIektCESdCGVK9a4wRB/bbjUYl+b7oAoGCCqGSM49\nAwEHoUQDQgAEUuLLJUJZ9cOPmYoP9Oapa6hwwhkzFZCMlD+GKujfW+Uon8o2iyKD\nOeQqSAO3oh7UVqoHsB/tbh0dcIVqNovr/w==\n-----END EC PRIVATE KEY-----\n', '-----BEGIN PUBLIC KEY-----\nMFkwEwYHKoZIzj0CAQYIKoZIzj0DAQcDQgAEUuLLJUJZ9cOPmYoP9Oapa6hwwhkz\nFZCMlD+GKujfW+Uon8o2iyKDOeQqSAO3oh7UVqoHsB/tbh0dcIVqNovr/w==\n-----END PUBLIC KEY-----\n', 0);

-- --------------------------------------------------------

--
-- Table structure for table `tb_sttd`
--

CREATE TABLE `tb_sttd` (
  `mid` varchar(256) NOT NULL,
  `filename` varchar(256) NOT NULL,
  `hvalue` text NOT NULL,
  `sigkey` text NOT NULL,
  `skey` text NOT NULL,
  `pkey` text NOT NULL,
  `nsig` int(11) NOT NULL,
  `nsed` int(11) NOT NULL,
  `uid1` int(11) DEFAULT NULL,
  `tsig1` timestamp NULL DEFAULT current_timestamp(),
  `uid2` int(11) DEFAULT NULL,
  `tsig2` timestamp NULL DEFAULT current_timestamp(),
  `uid3` int(11) DEFAULT NULL,
  `tsig3` timestamp NULL DEFAULT current_timestamp(),
  `uid4` int(11) DEFAULT NULL,
  `tsig4` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `tb_ttd`
--

CREATE TABLE `tb_ttd` (
  `id_t` varchar(256) NOT NULL,
  `namafile` varchar(255) NOT NULL,
  `hvalue` text NOT NULL,
  `pkey` text NOT NULL,
  `tsign` timestamp NOT NULL DEFAULT current_timestamp(),
  `id_p` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `tb_ttd`
--

INSERT INTO `tb_ttd` (`id_t`, `namafile`, `hvalue`, `pkey`, `tsign`, `id_p`) VALUES
('1', 'Gmail_-_Windows_10_Home_RETAIL_signed_by_astra.pdf', '2183d474be12124569770b4bfe95f320b12e4174ddd3048a7cb49c36e1bcdf11', '52e2cb254259f5c38f998a0ff4e6a96ba870c2193315908c943f862ae8df5be5289fca368b228339e42a4803b7a21ed456aa07b01fed6e1d1d70856a368bebff', '2024-02-12 07:14:53', 815861764),
('2', 'chrome_signed_by_astra.pdf', '20f2a4e3355a22e4983acb453152dfd1ea7c80b5eab3d5dabce4a5710acd5575', '52e2cb254259f5c38f998a0ff4e6a96ba870c2193315908c943f862ae8df5be5289fca368b228339e42a4803b7a21ed456aa07b01fed6e1d1d70856a368bebff', '2024-02-12 07:22:18', 815861764),
('Gmail_-_Lisensi_Project_2021_signed_by_astra_062ebf6e-c97a-11ee-ad5e-f8e43b2ff845', 'Gmail_-_Lisensi_Project_2021_signed_by_astra.pdf', '4a4862baefd62f5915605724e51ab56ec524d50c793ab08a029c6f023b3c379e', '52e2cb254259f5c38f998a0ff4e6a96ba870c2193315908c943f862ae8df5be5289fca368b228339e42a4803b7a21ed456aa07b01fed6e1d1d70856a368bebff', '2024-02-12 07:40:43', 815861764);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `tb_dk`
--
ALTER TABLE `tb_dk`
  ADD PRIMARY KEY (`id_k`);

--
-- Indexes for table `tb_pengguna`
--
ALTER TABLE `tb_pengguna`
  ADD PRIMARY KEY (`id_p`);

--
-- Indexes for table `tb_sttd`
--
ALTER TABLE `tb_sttd`
  ADD PRIMARY KEY (`mid`);

--
-- Indexes for table `tb_ttd`
--
ALTER TABLE `tb_ttd`
  ADD PRIMARY KEY (`id_t`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `tb_dk`
--
ALTER TABLE `tb_dk`
  MODIFY `id_k` int(11) NOT NULL AUTO_INCREMENT;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
