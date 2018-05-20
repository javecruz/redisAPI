-- phpMyAdmin SQL Dump
-- version 4.4.14
-- http://www.phpmyadmin.net
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 12-02-2018 a las 17:56:41
-- Versión del servidor: 5.6.26
-- Versión de PHP: 5.6.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `empresa`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `cliente`
--

CREATE TABLE IF NOT EXISTS `cliente` (
  `id` tinyint(7) NOT NULL,
  `nombres` varchar(50) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `ciudad` varchar(50) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `sexo` char(1) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `telefono` varchar(10) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `fecha_nacimiento` datetime NOT NULL,
  `direccion` varchar(100) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `provincia` varchar(100) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `fechaAlta` datetime NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `cliente`
--

INSERT INTO `cliente` (`id`, `nombres`, `ciudad`, `sexo`, `telefono`, `fecha_nacimiento`, `direccion`, `provincia`, `fechaAlta`) VALUES
(1, 'Javier', 'Valencia', 'M', '555444777', '2018-02-08 00:00:00', 'Esteban Dolz del Castellar', 'Valencia', '2018-02-11 13:34:35'),
(2, 'Pepe', 'Madrid', 'M', '111237713', '2018-02-08 00:00:00', 'Avenida Peset Aleixandre', 'Valencai', '2018-02-11 13:34:54'),
(3, 'Jorgee', 'Castellon', 'M', '555555555', '2018-02-01 00:00:00', 'Calle las nenas', 'Valencia', '2018-02-11 13:38:07'),
(4, 'Paca', 'Barcelona', 'M', '666555444', '2018-02-15 00:00:00', 'Avenida Diagonal', 'Barcelona', '2018-02-11 13:39:55');

--
-- Disparadores `cliente`
--
DELIMITER $$
CREATE TRIGGER `setFechaAlta` BEFORE INSERT ON `cliente`
 FOR EACH ROW BEGIN
    SET NEW.fechaAlta = NOW();
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ficheros`
--

CREATE TABLE IF NOT EXISTS `ficheros` (
  `id` int(11) NOT NULL,
  `nombre` varchar(150) NOT NULL,
  `tipo` varchar(55) NOT NULL,
  `id_Vehiculo` int(11) NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `ficheros`
--

INSERT INTO `ficheros` (`id`, `nombre`, `tipo`, `id_Vehiculo`) VALUES
(1, 'facturaFord-123123.pdf', 'Factura', 1),
(2, 'SCAnia-123123.pdf', 'Baja', 1),
(3, 'oooooo-123123.pdf', 'Factura', 2),
(4, 'fffff-123123.pdf', 'Contrato', 5),
(12, 'Fundamentos_de_jQuery-1518450856.pdf', 'Alta', 5),
(13, 'avionacoo-1518451218.jpg', 'Baja', 3),
(15, 'Fundamentos_de_jQuery-1518450856-1518452937.pdf', 'Baja', 5),
(16, '55Learning  Javascript Design Patterns-1518453115.pdf', 'Seguro', 10),
(17, 'Fundamentos_de_jQuery-1518454452.pdf', 'Incidencia', 11);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `vehiculos`
--

CREATE TABLE IF NOT EXISTS `vehiculos` (
  `id` int(11) NOT NULL,
  `matricula` varchar(20) NOT NULL,
  `fecha_fabricacion` datetime NOT NULL,
  `marca` varchar(55) NOT NULL,
  `modelo` varchar(50) NOT NULL,
  `id_cliente` tinyint(7) NOT NULL,
  `Tipo` tinyint(7) NOT NULL
) ENGINE=InnoDB AUTO_INCREMENT=12 DEFAULT CHARSET=latin1;

--
-- Volcado de datos para la tabla `vehiculos`
--

INSERT INTO `vehiculos` (`id`, `matricula`, `fecha_fabricacion`, `marca`, `modelo`, `id_cliente`, `Tipo`) VALUES
(1, '1111', '1111-11-11 00:00:00', 'Ford', 'Focussss', 1, 4),
(2, '66666', '2018-02-21 00:00:00', 'Seat', 'Toledo', 1, 3),
(3, '435', '2018-02-08 00:00:00', 'Forgdfgd', 'Focssus', 3, 2),
(4, '6456', '2018-02-21 00:00:00', 'Seasdat', 'Tolsadedo', 2, 4),
(5, 'zzzzz', '2018-02-08 00:00:00', 'Jackson', 'Tres', 1, 4),
(6, 'tttt', '2018-02-07 00:00:00', 'gggg', 'jjjj', 4, 3),
(9, 'sadasd', '2018-02-12 00:00:00', 'adsad', 'asdasd', 1, 2),
(10, 'dfdsf', '2018-02-09 00:00:00', 'fdvdcfg', 'sfdf', 1, 2),
(11, '777j', '2018-02-07 00:00:00', 'Ford', 'Tres', 3, 3);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `cliente`
--
ALTER TABLE `cliente`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id` (`id`);

--
-- Indices de la tabla `ficheros`
--
ALTER TABLE `ficheros`
  ADD PRIMARY KEY (`id`),
  ADD KEY `cascade` (`id_Vehiculo`);

--
-- Indices de la tabla `vehiculos`
--
ALTER TABLE `vehiculos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `cascadeDelete` (`id_cliente`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `cliente`
--
ALTER TABLE `cliente`
  MODIFY `id` tinyint(7) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=5;
--
-- AUTO_INCREMENT de la tabla `ficheros`
--
ALTER TABLE `ficheros`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=18;
--
-- AUTO_INCREMENT de la tabla `vehiculos`
--
ALTER TABLE `vehiculos`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT,AUTO_INCREMENT=12;
--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `ficheros`
--
ALTER TABLE `ficheros`
  ADD CONSTRAINT `cascade` FOREIGN KEY (`id_Vehiculo`) REFERENCES `vehiculos` (`id`) ON DELETE CASCADE;

--
-- Filtros para la tabla `vehiculos`
--
ALTER TABLE `vehiculos`
  ADD CONSTRAINT `cascadeDelete` FOREIGN KEY (`id_cliente`) REFERENCES `cliente` (`id`) ON DELETE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
