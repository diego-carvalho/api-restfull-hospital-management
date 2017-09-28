-- phpMyAdmin SQL Dump
-- version 4.5.4.1deb2ubuntu2
-- http://www.phpmyadmin.net
--
-- Host: localhost
-- Generation Time: 28-Set-2017 às 18:42
-- Versão do servidor: 5.7.19-0ubuntu0.16.04.1
-- PHP Version: 7.0.22-0ubuntu0.16.04.1

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `api-hospital`
--

-- --------------------------------------------------------

--
-- Estrutura da tabela `address`
--

CREATE TABLE `address` (
  `id` int(11) NOT NULL,
  `cep` varchar(20) NOT NULL,
  `state` varchar(2) NOT NULL,
  `city` varchar(150) NOT NULL,
  `neighborhood` varchar(150) NOT NULL,
  `street` varchar(150) NOT NULL,
  `number` int(11) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Extraindo dados da tabela `address`
--

INSERT INTO `address` (`id`, `cep`, `state`, `city`, `neighborhood`, `street`, `number`, `user_id`) VALUES
(1, '36300000', 'MG', 'SJDR', 'Tejuco', 'Bc', 11, 10);

-- --------------------------------------------------------

--
-- Estrutura da tabela `doctors`
--

CREATE TABLE `doctors` (
  `id` int(11) NOT NULL,
  `specialty` varchar(150) NOT NULL,
  `registry` varchar(100) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Extraindo dados da tabela `doctors`
--

INSERT INTO `doctors` (`id`, `specialty`, `registry`, `user_id`) VALUES
(1, 'neurocirurgião', 'crm-555', 10),
(4, 'neurocirurgião', 'crm-1255', 10);

-- --------------------------------------------------------

--
-- Estrutura da tabela `history`
--

CREATE TABLE `history` (
  `id` int(11) NOT NULL,
  `date` date NOT NULL,
  `disease` varchar(150) NOT NULL,
  `treatment` varchar(250) NOT NULL,
  `result` varchar(250) NOT NULL,
  `observation` varchar(250) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Extraindo dados da tabela `history`
--

INSERT INTO `history` (`id`, `date`, `disease`, `treatment`, `result`, `observation`, `user_id`) VALUES
(1, '1992-12-25', 'gripe', 'soro', 'curou', 'nenhuma', 10);

-- --------------------------------------------------------

--
-- Estrutura da tabela `hospitalized`
--

CREATE TABLE `hospitalized` (
  `id` int(11) NOT NULL,
  `start_date` datetime NOT NULL,
  `end_date` datetime NOT NULL,
  `local_id` int(11) NOT NULL,
  `patient_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Extraindo dados da tabela `hospitalized`
--

INSERT INTO `hospitalized` (`id`, `start_date`, `end_date`, `local_id`, `patient_id`) VALUES
(1, '2011-12-18 13:17:17', '2011-12-25 13:17:17', 1, 10);

-- --------------------------------------------------------

--
-- Estrutura da tabela `local`
--

CREATE TABLE `local` (
  `id` int(11) NOT NULL,
  `block` varchar(30) NOT NULL,
  `number` varchar(15) NOT NULL,
  `type` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Extraindo dados da tabela `local`
--

INSERT INTO `local` (`id`, `block`, `number`, `type`) VALUES
(1, 'B', '13-A', 'leito');

-- --------------------------------------------------------

--
-- Estrutura da tabela `nurses`
--

CREATE TABLE `nurses` (
  `id` int(11) NOT NULL,
  `registry` varchar(100) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Extraindo dados da tabela `nurses`
--

INSERT INTO `nurses` (`id`, `registry`, `user_id`) VALUES
(1, 'cre-55332', 10);

-- --------------------------------------------------------

--
-- Estrutura da tabela `phones`
--

CREATE TABLE `phones` (
  `id` int(11) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Extraindo dados da tabela `phones`
--

INSERT INTO `phones` (`id`, `phone`, `user_id`) VALUES
(8, '3233717171', 10),
(9, '3299771122', 10);

-- --------------------------------------------------------

--
-- Estrutura da tabela `procedures`
--

CREATE TABLE `procedures` (
  `id` int(11) NOT NULL,
  `type` varchar(150) NOT NULL,
  `date` datetime NOT NULL,
  `local_id` int(11) NOT NULL,
  `patient_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Extraindo dados da tabela `procedures`
--

INSERT INTO `procedures` (`id`, `type`, `date`, `local_id`, `patient_id`) VALUES
(1, 'cirurgia do olho', '2011-12-18 13:17:17', 1, 10),
(3, 'cirurgia cardiaca', '2011-12-18 13:17:17', 1, 10),
(4, 'cirurgia cardiaca', '2011-12-18 13:17:17', 1, 10),
(6, 'cirurgia cardiaca', '2011-12-18 13:17:17', 1, 10);

-- --------------------------------------------------------

--
-- Estrutura da tabela `schedules`
--

CREATE TABLE `schedules` (
  `id` int(11) NOT NULL,
  `date` date NOT NULL,
  `start_time` time NOT NULL,
  `end_time` time NOT NULL,
  `function` varchar(200) NOT NULL,
  `procedure_id` int(11) NOT NULL,
  `type_official` int(11) NOT NULL COMMENT '1=>doctor, 2=>nurse, 3=>student',
  `official_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Extraindo dados da tabela `schedules`
--

INSERT INTO `schedules` (`id`, `date`, `start_time`, `end_time`, `function`, `procedure_id`, `type_official`, `official_id`) VALUES
(1, '2011-12-18', '13:17:17', '20:17:17', 'Realizar a cirurgia', 1, 1, 1);

-- --------------------------------------------------------

--
-- Estrutura da tabela `students`
--

CREATE TABLE `students` (
  `id` int(11) NOT NULL,
  `institution` varchar(250) NOT NULL,
  `period` int(11) NOT NULL,
  `user_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Extraindo dados da tabela `students`
--

INSERT INTO `students` (`id`, `institution`, `period`, `user_id`) VALUES
(3, 'UFSJ', 8, 10),
(4, 'UFSJ', 6, 10);

-- --------------------------------------------------------

--
-- Estrutura da tabela `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `login` varchar(25) NOT NULL,
  `password` varchar(255) NOT NULL,
  `name` varchar(150) NOT NULL,
  `cpf` char(11) NOT NULL,
  `email` varchar(80) NOT NULL,
  `birthday` date NOT NULL,
  `admin` int(1) NOT NULL DEFAULT '0',
  `doctor` int(1) NOT NULL DEFAULT '0',
  `nurse` int(1) NOT NULL DEFAULT '0',
  `student` int(1) NOT NULL DEFAULT '0',
  `patient` int(1) NOT NULL DEFAULT '0',
  `council_president` int(1) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- Extraindo dados da tabela `users`
--

INSERT INTO `users` (`id`, `login`, `password`, `name`, `cpf`, `email`, `birthday`, `admin`, `doctor`, `nurse`, `student`, `patient`, `council_president`) VALUES
(10, 'diego', 'senhadiego', 'Diego', '09236243195', 'diego@gmail.com', '1992-12-25', 1, 1, 0, 0, 0, 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `address`
--
ALTER TABLE `address`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id_fk` (`user_id`);

--
-- Indexes for table `doctors`
--
ALTER TABLE `doctors`
  ADD PRIMARY KEY (`id`),
  ADD KEY `doctor_user_fk` (`user_id`) USING BTREE;

--
-- Indexes for table `history`
--
ALTER TABLE `history`
  ADD PRIMARY KEY (`id`),
  ADD KEY `history_user_fk` (`user_id`) USING BTREE;

--
-- Indexes for table `hospitalized`
--
ALTER TABLE `hospitalized`
  ADD PRIMARY KEY (`id`),
  ADD KEY `hospitalized_user_fk` (`patient_id`),
  ADD KEY `hospitalized_local_fk` (`local_id`) USING BTREE;

--
-- Indexes for table `local`
--
ALTER TABLE `local`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `nurses`
--
ALTER TABLE `nurses`
  ADD PRIMARY KEY (`id`),
  ADD KEY `nurse_user_fk` (`user_id`) USING BTREE;

--
-- Indexes for table `phones`
--
ALTER TABLE `phones`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id_fk` (`user_id`) USING BTREE;

--
-- Indexes for table `procedures`
--
ALTER TABLE `procedures`
  ADD PRIMARY KEY (`id`),
  ADD KEY `procedure_lodal_fk` (`local_id`) USING BTREE,
  ADD KEY `procedure_patient_fk` (`patient_id`) USING BTREE;

--
-- Indexes for table `schedules`
--
ALTER TABLE `schedules`
  ADD PRIMARY KEY (`id`),
  ADD KEY `official_users_fk` (`official_id`),
  ADD KEY `schedule_procedure_fk` (`procedure_id`) USING BTREE;

--
-- Indexes for table `students`
--
ALTER TABLE `students`
  ADD PRIMARY KEY (`id`),
  ADD KEY `student_user_fk` (`user_id`) USING BTREE;

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `address`
--
ALTER TABLE `address`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT for table `doctors`
--
ALTER TABLE `doctors`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
--
-- AUTO_INCREMENT for table `history`
--
ALTER TABLE `history`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT for table `hospitalized`
--
ALTER TABLE `hospitalized`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
--
-- AUTO_INCREMENT for table `local`
--
ALTER TABLE `local`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT for table `nurses`
--
ALTER TABLE `nurses`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
--
-- AUTO_INCREMENT for table `phones`
--
ALTER TABLE `phones`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;
--
-- AUTO_INCREMENT for table `procedures`
--
ALTER TABLE `procedures`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
--
-- AUTO_INCREMENT for table `schedules`
--
ALTER TABLE `schedules`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;
--
-- AUTO_INCREMENT for table `students`
--
ALTER TABLE `students`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;
--
-- Constraints for dumped tables
--

--
-- Limitadores para a tabela `address`
--
ALTER TABLE `address`
  ADD CONSTRAINT `address_user-fk` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Limitadores para a tabela `doctors`
--
ALTER TABLE `doctors`
  ADD CONSTRAINT `doctor_user_fk` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Limitadores para a tabela `history`
--
ALTER TABLE `history`
  ADD CONSTRAINT `history_user_fk` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Limitadores para a tabela `hospitalized`
--
ALTER TABLE `hospitalized`
  ADD CONSTRAINT `hospitalized_local_fk` FOREIGN KEY (`local_id`) REFERENCES `local` (`id`),
  ADD CONSTRAINT `hospitalized_user_fk` FOREIGN KEY (`patient_id`) REFERENCES `users` (`id`);

--
-- Limitadores para a tabela `nurses`
--
ALTER TABLE `nurses`
  ADD CONSTRAINT `nurse_user_fk` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Limitadores para a tabela `phones`
--
ALTER TABLE `phones`
  ADD CONSTRAINT `phone_user_fk` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Limitadores para a tabela `procedures`
--
ALTER TABLE `procedures`
  ADD CONSTRAINT `procedure_local_fk` FOREIGN KEY (`local_id`) REFERENCES `local` (`id`),
  ADD CONSTRAINT `procedure_patient_fk` FOREIGN KEY (`patient_id`) REFERENCES `users` (`id`);

--
-- Limitadores para a tabela `schedules`
--
ALTER TABLE `schedules`
  ADD CONSTRAINT `schedule_procedure_fk` FOREIGN KEY (`procedure_id`) REFERENCES `procedures` (`id`);

--
-- Limitadores para a tabela `students`
--
ALTER TABLE `students`
  ADD CONSTRAINT `student_user_fk` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
