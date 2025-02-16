DROP TABLE IF EXISTS `parents`;

CREATE TABLE `parents` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `student_name` varchar(20) DEFAULT '',
  `parent_name` varchar(20) DEFAULT NULL,
  `parent_mobile` varchar(10) DEFAULT NULL,
  `address` varchar(100) DEFAULT NULL
  PRIMARY KEY (`id`)
);

DROP TABLE IF EXISTS `students`;

CREATE TABLE `students` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(20) DEFAULT NULL,
  `score` int(11) DEFAULT NULL,
  `teacher_note` text,
  `class_name` varchar(10) DEFAULT NULL
  PRIMARY KEY (`id`)
);

DROP TABLE IF EXISTS `teachers`;

CREATE TABLE `teachers` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(20) DEFAULT NULL,
  `teachers` varchar(20) DEFAULT NULL,
  PRIMARY KEY (`id`)
);

-- INSERT INTO `parents` (`id`, `student_name`, `parent_name`, `parent_mobile`)
-- VALUES
--   (1,'Alex','Barry','0881234567'),
--   (2,'Alice','Jessica','0891234567'),
--   (3,'Jack','Simon','0876666666'),
--   (5,'Ophelia','Tracy','0881111111');


-- INSERT INTO `students` (`id`, `name`, `score`, `teacher_note`)
-- VALUES
--   (1,'Alex',100,'Alex did perfectly every day in the class. There is no surprise he got the full mark.'),
--   (2,'Alice',70,'Alice needs a lot of improvements.'),
--   (3,'Jack',75,'Even its not the best, Jack has already improved. Keep going.'),
--   (4,'Ophelia',0,'Unfortunately, Ophelia missed the test.'),
--   (5,'Zack',60,'Zack needs to do better.');