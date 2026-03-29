-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: localhost
-- Tiempo de generación: 29-03-2026 a las 19:53:25
-- Versión del servidor: 10.4.28-MariaDB
-- Versión de PHP: 8.1.17

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `illi_lia`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pedidos`
--

CREATE TABLE `pedidos` (
  `id_pedido` int(11) NOT NULL,
  `id_usuario` int(11) NOT NULL,
  `id_producto` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL DEFAULT 1,
  `total` decimal(10,2) NOT NULL,
  `estado` varchar(20) NOT NULL DEFAULT 'pendiente',
  `fecha` timestamp NOT NULL DEFAULT current_timestamp(),
  `comprobante` varchar(200) DEFAULT NULL,
  `metodo_pago` varchar(50) DEFAULT 'contra entrega'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `pedidos`
--

INSERT INTO `pedidos` (`id_pedido`, `id_usuario`, `id_producto`, `cantidad`, `total`, `estado`, `fecha`, `comprobante`, `metodo_pago`) VALUES
(1, 14, 6, 2, 7.00, 'completado', '2026-03-29 15:05:46', 'c6a914dc1cd649d2bcf42e46898ba01d.jpeg', 'pichincha'),
(2, 15, 1, 1, 8.50, 'completado', '2026-03-29 15:21:36', '5ff7894a64c04142a0537bd8c75aac7b.jpeg', 'produbanco');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `id_producto` int(11) NOT NULL,
  `nombre` varchar(100) DEFAULT NULL,
  `precio` decimal(10,2) DEFAULT NULL,
  `cantidad` int(11) DEFAULT NULL,
  `descripcion` text DEFAULT NULL,
  `imagen` varchar(200) DEFAULT NULL,
  `categoria` varchar(50) DEFAULT 'general'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `productos`
--

INSERT INTO `productos` (`id_producto`, `nombre`, `precio`, `cantidad`, `descripcion`, `imagen`, `categoria`) VALUES
(1, 'Jabon Mar y Cielo', 8.50, 6, 'Relajante y suavizante', 'jabon1.png', 'decorativo'),
(2, 'Jabon de Rosa Mosqueta', 9.00, 3, 'Exfoliante y nutritivo con miel pura y copos de avena.', 'jabon7.jpeg', 'nutritivo'),
(3, 'Jabon Galleta de Jengibre', 10.00, 3, 'Regenerador y antioxidante', 'jabon3.png', 'decorativo'),
(4, 'Jabon Dia de las Madres', 7.50, 14, 'Hidratante profundo', 'jabon4.png', 'decorativo'),
(6, 'Jabón de manzanilla', 3.50, 2, 'Calmante y suavizante con flores de manzanilla. Ideal para pieles sensibles.', 'jabon10.jpeg', 'nutritivo'),
(7, 'Jabon de Lavanda', 9.50, 10, 'Relajante y aromatico con flores de lavanda y pan de oro.', 'jabon6.jpeg', 'floral'),
(8, 'Jabon de Calendula', 9.50, 10, 'Calmante y nutritivo con flores de calendula y pan de oro.', 'jabon5.jpeg', 'floral'),
(9, 'Jabon de Cafe, Cacao y Canela', 10.50, 10, 'Energizante y exfoliante con cafe, cacao y canela. Ideal para activar la circulacion.', 'jabon9.jpeg', 'nutritivo'),
(10, 'Jabon de Almendra', 9.50, 10, 'Suavizante e hidratante con aceite de almendra dulce. Perfecto para pieles secas.', 'jabon8.jpeg', 'nutritivo');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuarios`
--

CREATE TABLE `usuarios` (
  `id_usuario` int(11) NOT NULL,
  `nombre` varchar(100) DEFAULT NULL,
  `mail` varchar(100) DEFAULT NULL,
  `password` varchar(255) DEFAULT NULL,
  `rol` varchar(20) NOT NULL DEFAULT 'cliente',
  `telefono` varchar(20) DEFAULT NULL,
  `direccion` varchar(200) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `usuarios`
--

INSERT INTO `usuarios` (`id_usuario`, `nombre`, `mail`, `password`, `rol`, `telefono`, `direccion`) VALUES
(13, 'lia', 'illilia0907@gmail.com', 'pbkdf2:sha256:1000000$eVa9VZGqjO0YWRkD$1e42be79f294796e0f2b3ca2e39cb664b507fdb50719cd881b5a139bb056b96c', 'admin', NULL, NULL),
(14, 'marina', 'flor@gmail.com', 'pbkdf2:sha256:1000000$vAEQnCbng5W01K5g$9dde8280f84e46daa8e21efb5dfca43b48cc8ae8ef900b63d6eedc884babd65b', 'cliente', NULL, NULL),
(15, 'SELENA', 'gsmedina@gmail.com', 'pbkdf2:sha256:1000000$Vp3ityWlNyRWDWm5$9f433bc113779ccfe7024ca384fca5a4b93fa2e76b9ecabf5cad01240d9c6e49', 'cliente', NULL, NULL);

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `pedidos`
--
ALTER TABLE `pedidos`
  ADD PRIMARY KEY (`id_pedido`),
  ADD KEY `id_usuario` (`id_usuario`),
  ADD KEY `id_producto` (`id_producto`);

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`id_producto`);

--
-- Indices de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  ADD PRIMARY KEY (`id_usuario`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `pedidos`
--
ALTER TABLE `pedidos`
  MODIFY `id_pedido` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT de la tabla `productos`
--
ALTER TABLE `productos`
  MODIFY `id_producto` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT de la tabla `usuarios`
--
ALTER TABLE `usuarios`
  MODIFY `id_usuario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `pedidos`
--
ALTER TABLE `pedidos`
  ADD CONSTRAINT `pedidos_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuarios` (`id_usuario`) ON DELETE CASCADE,
  ADD CONSTRAINT `pedidos_ibfk_2` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`) ON DELETE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
