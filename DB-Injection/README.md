```markdown
# 📦 Django Database Export & Import

Easily export and import your Django database using built-in management commands.

---

## 🚀 Export Database to JSON

Export all data from your database into a single JSON file:
```bash
python manage.py dumpdata > db.json
```

Export data from a specific app or model:
```bash
python manage.py dumpdata app_label.ModelName > model.json
# Example:
python manage.py dumpdata auth.User > users.json
```

---

## 📥 Import Database from JSON

Load data from a JSON file into your database:
```bash
python manage.py loaddata db.json
```
> **Note:**  
> Make sure all migrations have been applied and the models exist before running `loaddata`.

---

## ⚡️ Tips

- Run migrations before importing data:
  ```bash
  python manage.py migrate
  ```
- Version your data files or include them in your fixtures directory for easier testing and deployment.
- Use descriptive names for your JSON files to organize fixtures by app or model.

---

Happy coding! ✨
```
