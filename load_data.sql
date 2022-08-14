-- phpMyAdmin SQL Dump
-- version 4.6.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Server version: 5.7.14
-- PHP Version: 5.6.25

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `_databases_427`
--

--
-- Dumping data for table `airline`
--

INSERT INTO `airline` (`airline_name`) VALUES
('Pearl Airways'),
('Transaero Airlines'),
('USA3000 Airlines'),
('US Airways');

--
-- Dumping data for table `airline_staff`
--

INSERT INTO `airline_staff` (`username`, `password`, `first_name`, `last_name`, `date_of_birth`, `airline_name`) VALUES
('AirlineStaff', 'e19d5cd5af0378da05f63f891c7467af', 'Joe', 'Bland', '1980-02-05', 'Pearl Airways');

--
-- Dumping data for table `airplane`
--

INSERT INTO `airplane` (`airline_name`, `airplane_id`, `seats`) VALUES
('Pearl Airways', 1, 100),
('Transaero Airlines', 2, 10),
('USA3000 Airlines', 3, 700),
('US Airways', 4, 1600);

--
-- Dumping data for table `airport`
--

INSERT INTO `airport` (`airport_name`, `airport_city`) VALUES
('DTW', 'Detroit'),
('SMF', 'Sacramento'),
('MCI', 'Kansas City'),
('ORD', 'Chicago'),
('RSW', 'Fort Myers'),
('PIT', 'Pittsburgh'),
('PHL', 'Philadelphia'),
('PBI', 'West Palm Beach');

--
-- Dumping data for table `booking_agent`
--

INSERT INTO `booking_agent` (`email`, `password`, `booking_agent_id`) VALUES
('Booking@agent.com', 'e19d5cd5af0378da05f63f891c7467af', 1),
('Professional@booking.com', 'e19d5cd5af0378da05f63f891c7467af', 2);

--
-- Dumping data for table `customer`
--

INSERT INTO `customer` (`email`, `name`, `password`, `building_number`, `street`, `city`, `state`, `phone_number`, `passport_number`, `passport_expiration`, `passport_country`, `date_of_birth`) VALUES
('Customer@nyu.edu', 'Customer', 'e19d5cd5af0378da05f63f891c7467af', '2', 'Metrotech', 'New York', 'New York', 51234, 'P123456', '2020-10-24', 'USA', '1990-04-01'),
('one@nyu.edu', 'One', '098f6bcd4621d373cade4e832627b4f6', '6', 'Metrotech', 'New York', 'New York', 59873, 'P53412', '2021-04-05', 'USA', '1990-04-04'),
('two@nyu.edu', 'Two', '098f6bcd4621d373cade4e832627b4f6', '5', 'Metrotech', 'New York', 'New York', 58123, 'P436246', '2027-04-20', 'USA', '1992-04-18');

--
-- Dumping data for table `flight`
--

INSERT INTO `flight` (`airline_name`, `flight_num`, `departure_airport`, `departure_time`, `arrival_airport`, `arrival_time`, `price`, `status`, `airplane_id`) VALUES
('Pearl Airways', 139, 'DTW', '2022-07-31 23:50:00', 'SMF', '2022-08-01 08:50:00', '274.208', 'Arrived', 1),
('Transaero Airlines', 296, 'ORD', '2022-08-10 12:00:00', 'MCI', '2022-08-10 14:00:00', '162.934', 'Upcoming', 2),
('USA3000 Airlines', 307, 'RSW', '2022-08-19 22:00:00', 'PIT', '2022-08-20 02:00:00', '181.276', 'Delayed', 3),
('US Airways', 455, 'PHL', '2022-08-25 05:00:00', 'PBI', '2022-08-25 07:00:00', '163.482', 'Upcoming', 4);

--
-- Dumping data for table `ticket`
--

INSERT INTO `ticket` (`ticket_id`, `airline_name`, `flight_num`) VALUES
(1, 'Pearl Airways', 139),
(2, 'Pearl Airways', 139),
(3, 'Transaero Airlines', 296),
(4, 'Transaero Airlines', 296),
(5, 'Transaero Airlines', 296),
(6, 'USA3000 Airlines', 307),
(7, 'USA3000 Airlines', 307),
(8, 'US Airways', 455),
(9, 'US Airways', 455);


--
-- Dumping data for table `purchases`
--

INSERT INTO `purchases` (`ticket_id`, `customer_email`, `booking_agent_id`, `purchase_date`) VALUES
(1, 'Customer@nyu.edu', NULL, '2022-08-01'),
(2, 'Customer@nyu.edu', 1, '2022-08-17'),
(3, 'one@nyu.edu', 2, '2022-06-10'),
(4, 'two@nyu.edu', 2, '2022-07-11'),
(5, 'Customer@nyu.edu', 1, '2022-08-12'),
(6, 'one@nyu.edu', null, '2022-05-19'),
(7, 'two@nyu.edu', null, '2022-06-23'),
(8, 'one@nyu.edu', 1, '2022-01-15'),
(9, 'Customer@nyu.edu', 1, '2022-06-19');


/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
