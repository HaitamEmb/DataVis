# DataViz Bi - Financial Transaction ETL & Clustering Pipeline

An end-to-end Data Engineering pipeline designed to ingest, clean, and segment financial transaction data using Unsupervised Machine Learning.

## Overview
In this project we automate the transition from "dirty" raw transaction logs to actionable customer segments. We handle everything from data validation and currency standardization to advanced outlier detection and automated clustering.

## Technical Architecture
1.  **Ingestion:** Python-driven extraction from raw CSV files.
2.  **Cleaning & Validation:** 
    * Standardization of transaction types and currency formatting.
    * **IQR Filtering:** Automated removal of statistical outliers using the Interquartile Range ($Q3 - Q1$).
3.  **Storage:** Loading into a **PostgreSQL** schema optimized with Primary/Foreign Key constraints.
4.  **Analytics:** 
    * **Frequency Distribution:** Visualized via dynamic histograms.
    * **K-Means Clustering:** Segmenting customers into behavioral profiles.
    * **Kneedle Algorithm:** Programmatic detection of the "Elbow Point" using the longest perpendicular line method.

## Tech Stack
* **Language:** Python 3.12.3, bash
* **Libraries:** Pandas, Matplotlib, Numpy, psycopg2
* **Database:** PostgreSQL (Relational modeling & Indexing)
* **DevOps/Tooling:** Makefile (Build automation), Git/GitHub

## Project Structure
| File | Description |
| :--- | :--- |
| **Makefile** | Orchestrates the entire pipeline; automates setup, database creation, and script execution. |
| **create_customer_table.sh** | Shell script to initialize the PostgreSQL schema for customer data. |
| **create_items_table.sh** | Shell script to initialize the PostgreSQL schema for transaction items. |
| **dup_remove.py** | Data cleaning script focused on identifying and removing duplicate records. |
| **elbow.py** | Core logic for the Elbow Method; implements the Kneedle algorithm (perpendicular distance). |
| **chart.py** | Generates standard data visualizations for exploratory analysis. |
| **pie.py** | Generates pie charts for categorical distribution of transactions. |
| **building.py** | Generates histogram/bar visualizations (the "building" shapes) for frequency analysis. |
| **mustache.py** | Generates Box Plots (the "mustache" plots) to visualize IQR and outliers. |
| **math_utilities.py** | Shared module containing custom mathematical functions and IQR calculations. |
| **env_setup.sh** | Automation script for setting up the local virtual environment and dependencies. |
| **requirements.txt** | List of Python dependencies (Pandas, Scikit-learn, etc.) required for the project. |

## Prerequisites

Before running this pipeline, ensure your local environment meets the following requirements. 

> **Note:** This project is currently **not dockerized**. All dependencies (including the database) must be installed and running on your host machine.

### 1. Software & Environment
* **Python 3.8+**: The core logic uses f-strings and type hinting available in modern Python versions.
* **PostgreSQL (v12+)**: A local PSQL instance must be running. You will need `createdb` permissions to initialize the schemas.
* **Bash/Unix Shell**: The automation scripts (`.sh` files) and the `Makefile` are designed for Unix-based environments (Linux, macOS, or WSL on Windows).
* **Dbeaver**: For visualization (optional)

### 2. System Tools
* **Make**: Used to run the `Makefile` commands.
* **Pip**: Ensure your Python package manager is up to date (`pip install --upgrade pip`).

### 3. Database Access
You must have a PostgreSQL user with the following capabilities:
* Connectivity via `localhost` (ensure your `pg_hba.conf` allows local connections).

### 4. Environment Variables
The pipeline expects a `.env` file in the root directory. Without this, the Python scripts will be unable to establish a connection to the database. (Refer to the **Configuration** section below for the template).

## Getting Started

Follow these steps to set up the environment and execute the pipeline from scratch.

### 1. Configure Environment Variables
The pipeline requires database credentials to communicate with PostgreSQL. Create a file named `.env` in the root directory and copy the following template:

```text
POSTGRES_USER=your_username
POSTGRES_PASSWORD=your_password
POSTGRES_DB=your_db_name
POSTGRES_HOST=localhost
```

### 2. Setup
```bash
git clone https://github.com/HaitamEmb/DataVis.git
cd DataVis
```

### 3. Make
```bash
make all
```

This command :
* Create Python virtual enviroment and insall all dependencies
* Start PostgreSQL
* Ingest CSV data into the database
* Remove duplicates
* Merge customers and items tables

### 4. Visualizations
```bash
source .venv/bin/activate

make pie #Generates pie charts for event distribution
make chart #Generates standard data visualizations
make mustache #Generates Box Plots
make building #Generates histogram/bar visualizations
make elbow #Generates Elbow Method graph
```

## Project Highlights
* ```math_utilities.py``` is a custom statistics library implemented from scratch, covering each of the Mean, variance, population standard deviation, quartiles, percentiles, min, max etc...
* ```elbow.py``` implements a custom K-Means algorithm.
* Automated ETL pipeline

## Cleanup
```bash
make fclean
```
Will thoroughly clean and delete all the previously generated files and directories.


#to add, Dbeaver visualization, and more on enviroment setup
