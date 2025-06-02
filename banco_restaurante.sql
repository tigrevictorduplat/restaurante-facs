-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Tempo de geração: 20/05/2025 às 19:17
-- Versão do servidor: 10.4.32-MariaDB
-- Versão do PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Banco de dados: `banco_restaurante`
--

-- --------------------------------------------------------

--
-- Estrutura para tabela `tb_mesas`
--

CREATE TABLE `tb_mesas` (
  `idMesa` int(100) NOT NULL,
  `statusMesaOcupada` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura para tabela `tb_reservas`
--

CREATE TABLE `tb_reservas` (
  `idReserva` int(100) NOT NULL,
  `dataReserva` date NOT NULL,
  `horaReserva` time NOT NULL,
  `nomeCliente` varchar(255) NOT NULL,
  `quantidadePessoas` int(20) NOT NULL,
  `statusReservaConfirmada` tinyint(1) NOT NULL DEFAULT 0,
  `idMesaReserva` int(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estrutura stand-in para view `vw_confirmacoes_por_mesa`
-- (Veja abaixo para a visão atual)
--
CREATE TABLE `vw_confirmacoes_por_mesa` (
`idMesa` int(100)
,`totalConfirmacoes` bigint(21)
);

-- --------------------------------------------------------

--
-- Estrutura stand-in para view `vw_reservas_por_data_e_status`
-- (Veja abaixo para a visão atual)
--
CREATE TABLE `vw_reservas_por_data_e_status` (
`dataReserva` date
,`statusReservaConfirmada` tinyint(1)
,`totalReservas` bigint(21)
);

-- --------------------------------------------------------

--
-- Estrutura stand-in para view `vw_reservas_por_mesa`
-- (Veja abaixo para a visão atual)
--
CREATE TABLE `vw_reservas_por_mesa` (
`idReserva` int(100)
,`dataReserva` date
,`horaReserva` time
,`idMesaReserva` int(100)
,`nomeCliente` varchar(255)
,`quantidadePessoas` int(20)
,`statusReservaConfirmada` tinyint(1)
);

-- --------------------------------------------------------

--
-- Estrutura para view `vw_confirmacoes_por_mesa`
--
DROP TABLE IF EXISTS `vw_confirmacoes_por_mesa`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_confirmacoes_por_mesa`  AS SELECT `tb_reservas`.`idMesaReserva` AS `idMesa`, count(0) AS `totalConfirmacoes` FROM `tb_reservas` WHERE `tb_reservas`.`statusReservaConfirmada` = 1 GROUP BY `tb_reservas`.`idMesaReserva` ;

-- --------------------------------------------------------

--
-- Estrutura para view `vw_reservas_por_data_e_status`
--
DROP TABLE IF EXISTS `vw_reservas_por_data_e_status`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_reservas_por_data_e_status`  AS SELECT `tb_reservas`.`dataReserva` AS `dataReserva`, `tb_reservas`.`statusReservaConfirmada` AS `statusReservaConfirmada`, count(0) AS `totalReservas` FROM `tb_reservas` GROUP BY `tb_reservas`.`dataReserva`, `tb_reservas`.`statusReservaConfirmada` ;

-- --------------------------------------------------------

--
-- Estrutura para view `vw_reservas_por_mesa`
--
DROP TABLE IF EXISTS `vw_reservas_por_mesa`;

CREATE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `vw_reservas_por_mesa`  AS SELECT `tb_reservas`.`idReserva` AS `idReserva`, `tb_reservas`.`dataReserva` AS `dataReserva`, `tb_reservas`.`horaReserva` AS `horaReserva`, `tb_reservas`.`idMesaReserva` AS `idMesaReserva`, `tb_reservas`.`nomeCliente` AS `nomeCliente`, `tb_reservas`.`quantidadePessoas` AS `quantidadePessoas`, `tb_reservas`.`statusReservaConfirmada` AS `statusReservaConfirmada` FROM `tb_reservas` ;

--
-- Índices para tabelas despejadas
--

--
-- Índices de tabela `tb_mesas`
--
ALTER TABLE `tb_mesas`
  ADD PRIMARY KEY (`idMesa`);

--
-- Índices de tabela `tb_reservas`
--
ALTER TABLE `tb_reservas`
  ADD PRIMARY KEY (`idReserva`),
  ADD KEY `keyMesaReserva` (`idMesaReserva`);

--
-- AUTO_INCREMENT para tabelas despejadas
--

--
-- AUTO_INCREMENT de tabela `tb_mesas`
--
ALTER TABLE `tb_mesas`
  MODIFY `idMesa` int(100) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de tabela `tb_reservas`
--
ALTER TABLE `tb_reservas`
  MODIFY `idReserva` int(100) NOT NULL AUTO_INCREMENT;

--
-- Restrições para tabelas despejadas
--

--
-- Restrições para tabelas `tb_reservas`
--
ALTER TABLE `tb_reservas`
  ADD CONSTRAINT `keyMesaReserva` FOREIGN KEY (`idMesaReserva`) REFERENCES `tb_mesas` (`idMesa`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
