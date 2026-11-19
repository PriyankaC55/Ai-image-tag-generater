

CREATE DATABASE IF NOT EXISTS `ai_image_tagger` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `ai_image_tagger`;


CREATE TABLE IF NOT EXISTS `users` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `username` VARCHAR(80) NOT NULL UNIQUE,
    `email` VARCHAR(120) NOT NULL UNIQUE,
    `password_hash` VARCHAR(255) NOT NULL,
    `is_admin` BOOLEAN DEFAULT FALSE,
    `theme_preference` VARCHAR(20) DEFAULT 'dark',
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX `idx_username` (`username`),
    INDEX `idx_email` (`email`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE IF NOT EXISTS `categories` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `name` VARCHAR(100) NOT NULL UNIQUE,
    `icon` VARCHAR(50) DEFAULT 'bi-tag',
    `description` TEXT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE IF NOT EXISTS `images` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NOT NULL,
    `filename` VARCHAR(255) NOT NULL,
    `original_path` VARCHAR(255) NOT NULL,
    `processed_path` VARCHAR(255) NULL,
    `thumbnail_path` VARCHAR(255) NULL,
    `file_size` INT NULL,
    `width` INT NULL,
    `height` INT NULL,
    `mime_type` VARCHAR(50) NULL,
    `blur_score` FLOAT NULL,
    `is_blurry` BOOLEAN DEFAULT FALSE,
    `image_hash` VARCHAR(64) NULL,
    `ai_caption` TEXT NULL,
    `category_name` VARCHAR(100) DEFAULT 'General',
    `analysis_status` VARCHAR(50) DEFAULT 'pending',
    `error_message` TEXT NULL,
    `detected_objects_count` INT DEFAULT 0,
    `tags_count` INT DEFAULT 0,
    `is_favorite` BOOLEAN DEFAULT FALSE,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX `idx_user_id` (`user_id`),
    INDEX `idx_image_hash` (`image_hash`),
    INDEX `idx_created_at` (`created_at`),
    CONSTRAINT `fk_images_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;


CREATE TABLE IF NOT EXISTS `generated_tags` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `image_id` INT NOT NULL,
    `category_id` INT NULL,
    `tag_name` VARCHAR(100) NOT NULL,
    `tag_kannada` VARCHAR(100) NULL,
    `tag_hindi` VARCHAR(100) NULL,
    `confidence` FLOAT DEFAULT 1.0,
    `source` VARCHAR(50) DEFAULT 'ai',
    `bounding_box` TEXT NULL,
    `is_custom` BOOLEAN DEFAULT FALSE,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX `idx_image_id` (`image_id`),
    INDEX `idx_category_id` (`category_id`),
    INDEX `idx_tag_name` (`tag_name`),
    CONSTRAINT `fk_tags_image` FOREIGN KEY (`image_id`) REFERENCES `images` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_tags_category` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `favorites` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NOT NULL,
    `image_id` INT NULL,
    `tag_id` INT NULL,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX `idx_fav_user` (`user_id`),
    INDEX `idx_fav_image` (`image_id`),
    INDEX `idx_fav_tag` (`tag_id`),
    CONSTRAINT `fk_fav_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_fav_image` FOREIGN KEY (`image_id`) REFERENCES `images` (`id`) ON DELETE CASCADE,
    CONSTRAINT `fk_fav_tag` FOREIGN KEY (`tag_id`) REFERENCES `generated_tags` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

CREATE TABLE IF NOT EXISTS `activity_logs` (
    `id` INT AUTO_INCREMENT PRIMARY KEY,
    `user_id` INT NULL,
    `action` VARCHAR(100) NOT NULL,
    `details` TEXT NULL,
    `ip_address` VARCHAR(45) NULL,
    `created_at` DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX `idx_log_user` (`user_id`),
    INDEX `idx_log_created` (`created_at`),
    CONSTRAINT `fk_logs_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT IGNORE INTO `categories` (`name`, `icon`, `description`) VALUES
('Objects', 'bi-box-seam', 'Physical everyday objects, items and tools'),
('Animals', 'bi-feather', 'Domestic pets, wild animals, birds and fauna'),
('People', 'bi-people', 'Humans, faces, portraits and crowds'),
('Vehicles', 'bi-car-front', 'Cars, bikes, trucks, planes and transit'),
('Nature & Landscape', 'bi-tree', 'Forests, parks, mountains, waters and skies'),
('Food & Drink', 'bi-cup-hot', 'Meals, snacks, beverages and ingredients'),
('Architecture & Places', 'bi-buildings', 'Buildings, monuments, interiors and urban scenes'),
('Activities & Sports', 'bi-trophy', 'Sports, actions, hobbies and movements'),
('Colors & Attributes', 'bi-palette', 'Visual shades, patterns and visual styles'),
('General', 'bi-tags', 'General contextual keywords and concepts');
