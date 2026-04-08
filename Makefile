

NAME	= dataviz

.PHONY: pie mustache building chart elbow dup_remove

fclean:
	-@rm -rf /data/data_proj/subject.zip
	-@rm -rf /data/data_proj/subject
	-@rm -rf /data/data_proj/data_test/data/subject.zip
	-@rm -rf /data/data_proj/data_test/data/subject
	-@rm -rf /data/data_proj/data_test/data/*.csv
	-@rm -rf /data/data_proj/data_test/data/*/*.csv
	-@rm -rf /data/data_proj/data_test/data/*.png
	-@rm -rf .venv
	-@rm -rf srcs/dist

login:
	postgresql sh -c 'psql -U $$POSTGRES_USER -d $$POSTGRES_DBB -W'

cusotmers:
	-@chmod +x ./create_customers_table.sh
	./create_customers_table.sh

dup_remove:
	-@chmod +x ./dup_remove.sh
	./dup_remove.sh

fusion:
	-@chmod +x ./create_items_table.sh
	./create_customers_table.sh

setup_env:
	-@mkdir -p /data/data_proj
	-@chmod +x ./env_setup.sh
	./env_setup.sh

setup_db:
	-@echo "Database creating..."
	-@chmod +x create_customers_table.sh dup_remove.sh create_items_table.sh
	./create_customers_table.sh && ./dup_remove.sh && create_items_table.sh
	-@echo "Database is created."

pie:
	-@chmod +x ./pie.py
	./pie.py

chart:
	-@chmod +x ./chart.py
	./chart.py

building:
	-@chmod +x ./building.py
	./building.py

elbow:
	-@chmod +x ./elbow.py
	./elbow.py

re: fclean all
	