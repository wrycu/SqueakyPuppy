CREATE TABLE `pos`.`sp_callbacks` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `callback` VARCHAR(1024) NOT NULL,
  PRIMARY KEY (`id`));

CREATE TABLE `pos`.`sp_users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `email` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`id`));

CREATE TABLE `pos`.`sp_assessments` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `date_started` DATETIME NOT NULL,
  PRIMARY KEY (`id`));

CREATE TABLE `sp_assessment_notify` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `an_user_idx` (`user_id`),
  CONSTRAINT `an_user` FOREIGN KEY (`user_id`) REFERENCES `sp_users` (`id`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

CREATE TABLE `pos`.`sp_hits` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `assessment_id` INT NOT NULL,
  `callback_id` INT NOT NULL,
  `referrer` VARCHAR(1024) NOT NULL,
  `date_captured` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`id`),
  INDEX `hit_ass_idx` (`assessment_id` ASC),
  INDEX `hit_callback_idx` (`callback_id` ASC),
  CONSTRAINT `hit_ass`
    FOREIGN KEY (`assessment_id`)
    REFERENCES `pos`.`sp_assessments` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `hit_callback`
    FOREIGN KEY (`callback_id`)
    REFERENCES `pos`.`sp_callbacks` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);

CREATE TABLE `pos`.`sp_blacklist` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `domain` VARCHAR(1024) NOT NULL,
  PRIMARY KEY (`id`));
