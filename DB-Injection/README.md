In Django, you can use the dumpdata and loaddata management commands to export and import your database to/from JSON format.

✅ Export Database to JSON
bash
Copy
Edit
python manage.py dumpdata > db.json
Exports all data from the database into a single JSON file.

If you only want data from a specific app or model:

bash
Copy
Edit
python manage.py dumpdata app_label.ModelName > model.json
Example:

bash
Copy
Edit
python manage.py dumpdata auth.User > users.json
✅ Import Database from JSON
bash
Copy
Edit
python manage.py loaddata db.json
Loads data from the given JSON file into the database.

Make sure the models already exist (i.e., migrations have been applied).

⚠️ Tips
Run python manage.py migrate before using loaddata.

You can version your data files or include them in fixtures for easy testing and deployment.
