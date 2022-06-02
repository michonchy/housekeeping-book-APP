```mermaid
erDiagram

users {
    INTEGER id
    TEXT name
}

categories {
    INTEGER id
    TEXT name
}

spendings {
    INTEGER id
    INTEGER amount
    TEXT date
    INTEGER user_id
    INTEGER category_id
}
spendings ||--|| users : has
spendings ||--|| categories : has

incomes {
    INTEGER id
    INTEGER amount
    TEXT date
    INTEGER user_id
    INTEGER category_id
}
incomes ||--|| users : has
incomes ||--|| categories : has

```

```
"||" -> 1
"--" -> テーブルを繋げる線
"o{" -> 0 or n
```

```sql
NULL       NULL値
INTEGER    符号付整数。1, 2, 3, 4, 6, or 8 バイトで格納
REAL       浮動小数点数。8バイトで格納
TEXT       テキスト。UTF-8, UTF-16BE or UTF-16-LEのいずれかで格納
BLOB       Binary Large OBject。入力データをそのまま格納
```