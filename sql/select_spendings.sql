SELECT spendings.id, spendings.amount, spendings.date, users.name, categories.name FROM spendings
  INNER JOIN users
  ON spendings.user_id = users.id
  INNER JOIN categories
  ON spendings.category_id = categories.id
  WHERE amount = 1001;