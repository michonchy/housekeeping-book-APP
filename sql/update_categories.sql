ALTER TABLE categories ADD COLUMN color TEXT DEFAULT '00AA00';
UPDATE categories SET color = '000000' WHERE id = 9;