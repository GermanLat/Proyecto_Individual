-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema proyecto_individual
-- -----------------------------------------------------
DROP SCHEMA IF EXISTS `proyecto_individual` ;

-- -----------------------------------------------------
-- Schema proyecto_individual
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `proyecto_individual` DEFAULT CHARACTER SET utf8 ;
USE `proyecto_individual` ;

-- -----------------------------------------------------
-- Table `proyecto_individual`.`natural_persons`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `proyecto_individual`.`natural_persons` ;

CREATE TABLE IF NOT EXISTS `proyecto_individual`.`natural_persons` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `identity_document` VARCHAR(15) NOT NULL,
  `first_name` VARCHAR(255) NOT NULL,
  `last_name` VARCHAR(255) NOT NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW(),
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `proyecto_individual`.`legal_persons`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `proyecto_individual`.`legal_persons` ;

CREATE TABLE IF NOT EXISTS `proyecto_individual`.`legal_persons` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NULL,
  `business_name` VARCHAR(255) NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW(),
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `proyecto_individual`.`users`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `proyecto_individual`.`users` ;

CREATE TABLE IF NOT EXISTS `proyecto_individual`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `natural_person_id` INT NULL,
  `legal_person_id` INT NULL,
  `email` VARCHAR(255) NULL,
  `ruc` VARCHAR(255) NULL,
  `password` VARCHAR(255) NOT NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW(),
  PRIMARY KEY (`id`),
  INDEX `fk_usuarios_natural_person1_idx` (`natural_person_id` ASC) VISIBLE,
  INDEX `fk_usuarios_legal_person1_idx` (`legal_person_id` ASC) VISIBLE,
  CONSTRAINT `fk_usuarios_natural_person1`
    FOREIGN KEY (`natural_person_id`)
    REFERENCES `proyecto_individual`.`natural_persons` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_usuarios_legal_person1`
    FOREIGN KEY (`legal_person_id`)
    REFERENCES `proyecto_individual`.`legal_persons` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `proyecto_individual`.`document_types`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `proyecto_individual`.`document_types` ;

CREATE TABLE IF NOT EXISTS `proyecto_individual`.`document_types` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW(),
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `proyecto_individual`.`documents`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `proyecto_individual`.`documents` ;

CREATE TABLE IF NOT EXISTS `proyecto_individual`.`documents` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `date` DATE NULL,
  `amount` INT NULL,
  `emitter_id` INT NOT NULL,
  `receiver_id` INT NOT NULL,
  `document_type_id` INT NOT NULL,
  `document_number` VARCHAR(255) NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW(),
  PRIMARY KEY (`id`),
  INDEX `fk_comprobantes_tipos_comprobantes1_idx` (`document_type_id` ASC) VISIBLE,
  INDEX `fk_comprobantes_usuarios1_idx` (`emitter_id` ASC) VISIBLE,
  INDEX `fk_comprobantes_users1_idx` (`receiver_id` ASC) VISIBLE,
  CONSTRAINT `fk_comprobantes_tipos_comprobantes1`
    FOREIGN KEY (`document_type_id`)
    REFERENCES `proyecto_individual`.`document_types` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_comprobantes_usuarios1`
    FOREIGN KEY (`emitter_id`)
    REFERENCES `proyecto_individual`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_comprobantes_users1`
    FOREIGN KEY (`receiver_id`)
    REFERENCES `proyecto_individual`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `proyecto_individual`.`transaction_types`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `proyecto_individual`.`transaction_types` ;

CREATE TABLE IF NOT EXISTS `proyecto_individual`.`transaction_types` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NOT NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW(),
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `proyecto_individual`.`transaction_categories`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `proyecto_individual`.`transaction_categories` ;

CREATE TABLE IF NOT EXISTS `proyecto_individual`.`transaction_categories` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(255) NULL,
  `transaction_type_id` INT NOT NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW(),
  PRIMARY KEY (`id`),
  INDEX `fk_categorias_transacciones_tipos_transacciones2_idx` (`transaction_type_id` ASC) VISIBLE,
  CONSTRAINT `fk_categorias_transacciones_tipos_transacciones2`
    FOREIGN KEY (`transaction_type_id`)
    REFERENCES `proyecto_individual`.`transaction_types` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `proyecto_individual`.`transactions`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `proyecto_individual`.`transactions` ;

CREATE TABLE IF NOT EXISTS `proyecto_individual`.`transactions` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `date` DATE NULL,
  `amount` INT NULL,
  `description` TEXT NULL,
  `document_id` INT NULL,
  `transaction_as_id` INT NOT NULL,
  `bill_of_id` INT NOT NULL,
  `transaction_category_id` INT NULL,
  `created_at` DATETIME NULL,
  `updated_at` DATETIME NULL,
  PRIMARY KEY (`id`),
  INDEX `fk_gastos_comprobantes1_idx` (`document_id` ASC) VISIBLE,
  INDEX `fk_gastos_usuarios1_idx` (`transaction_as_id` ASC) VISIBLE,
  INDEX `fk_gastos_usuarios2_idx` (`bill_of_id` ASC) VISIBLE,
  INDEX `fk_gastos_categorias1_idx` (`transaction_category_id` ASC) VISIBLE,
  CONSTRAINT `fk_gastos_comprobantes1`
    FOREIGN KEY (`document_id`)
    REFERENCES `proyecto_individual`.`documents` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_gastos_usuarios1`
    FOREIGN KEY (`transaction_as_id`)
    REFERENCES `proyecto_individual`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_gastos_usuarios2`
    FOREIGN KEY (`bill_of_id`)
    REFERENCES `proyecto_individual`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_gastos_categorias1`
    FOREIGN KEY (`transaction_category_id`)
    REFERENCES `proyecto_individual`.`transaction_categories` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `proyecto_individual`.`document_photos`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `proyecto_individual`.`document_photos` ;

CREATE TABLE IF NOT EXISTS `proyecto_individual`.`document_photos` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `document_id` INT NOT NULL,
  `path` VARCHAR(255) NOT NULL,
  `photographer_id` INT NOT NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NOW(),
  PRIMARY KEY (`id`),
  INDEX `fk_fotos_comprobantes_usuarios1_idx` (`photographer_id` ASC) VISIBLE,
  CONSTRAINT `fk_fotografias_comprobantes_comprobantes1`
    FOREIGN KEY (`document_id`)
    REFERENCES `proyecto_individual`.`documents` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_fotos_comprobantes_usuarios1`
    FOREIGN KEY (`photographer_id`)
    REFERENCES `proyecto_individual`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
