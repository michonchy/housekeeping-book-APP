SELECT incomes.id, incomes.amount, incomes.date, users.name, categories.name FROM incomes
  INNER JOIN users
  ON incomes.user_id = users.id
  INNER JOIN categories
  ON incomes.category_id = categories.id
  WHERE amount = 1000;