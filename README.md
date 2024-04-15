Flask example project


## run flask migration
1. `flask db init` - generate migration folder
2. `flask db stamp head` - update database 
3. `flask db migrate -m 'comment'` - autogenerate migration script
4. `flask db upgrade` - apply migration