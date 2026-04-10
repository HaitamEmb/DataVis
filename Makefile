

NAME	= dataviz

.PHONY: pie mustache building chart elbow dup_remove

all: prep

fclean:
	-@rm -rf data/data_proj/subject.zip
	-@rm -rf data/data_proj/subject
	-@rm -rf data/data_proj/data_test/data/subject.zip
	-@rm -rf data/data_proj/data_test/data/subject
	-@rm -rf data/data_proj/data_test/data/*.csv
	-@rm -rf data/data_proj/data_test/data/*/*.csv
	-@rm -rf data/data_proj/data_test/data/*.png
	-@rm -rf .venv
	-@rm -rf __pycache__ srcs/dist
	-@rm -rf srcs/dist
	-@rm -rf $(NAME)
	-@rm -rf data/
	-@rm -rf data_test/





login:
	postgresql sh -c 'psql -U $$POSTGRES_USER -d $$POSTGRES_DB -W'

customers:
	-@chmod +x ./create_customers_table.sh
	./create_customers_table.sh

dup_remove:
	-@chmod +x ./dup_remove.sh
	./dup_remove.sh

fusion:
	-@chmod +x ./create_items_table.sh
	./create_items_table.sh

setup_env:
	-@mkdir -p data/data_proj
	-@chmod +x ./env_setup.sh
	./env_setup.sh

setup_db:
	-@echo "Database creating..."
	-@chmod +x create_customers_table.sh dup_remove.sh create_items_table.sh
	./create_customers_table.sh && ./dup_remove.sh && ./create_items_table.sh
	-@echo "Database is created."

prep: setup_env setup_db

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
	