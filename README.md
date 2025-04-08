# Azure Data Pipeline

## Overview
This project uploads Community Development (CDD), Fire, Public Works (PW), and Police Department (PD) tables to Azure Data Lake Storage (ADLS).

## Project Structure
```
project_root/
│── config/
│   │── config.py              # Configuration loader
│   │── config_logging.py      # Logging setup
│   │── config.yaml            # Credentials
│── helpers/
│   │── sql_helpers.py         # Database connection and query execution
│   │── az_helpers.py          # Azure Data Lake upload utilities
│── main.py                    # Main execution script
│── README.md                  # Project documentation
```

## Dependencies
Install the dependencies from requirements.txt.

## Configuration
- Credentials and configurations are stored in config.yaml (you must add this file).
- Logging is set up using config_logging.py.

## Execution
Run the pipeline by executing:
```bash
py -m main
```

## Functionality
1. **Database Connection**
   - Connects to City of Stockton's OPDA, PD, and Fire databases.
   - Uses SQLAlchemy for database connections.

2. **Data Extraction**
   - Fetches data from predefined tables in different departments.
   - Queries are dynamically generated for table selection.

3. **Data Upload to Azure**
   - Converts extracted data to Parquet format.
   - Uploads the data to development and production ADLS containers.

## Table Mappings
### Community Development (CDD)
- accela_permit_cycles_prod
- accela_resubmittal_cycles_prod
- accela_tasks_prod
- accela_department_cycles_prod

### Fire Department
- EventList  
- Deep_Dive_TOT  
- 2024_Loss  
- 2023_Non_Homeless_Related  
- 2024_Non_Homeless_Related  
- 2023-2024_Homelessness  
- 2023_False_Alarms  
- 2023_Loss  
- 2023_Responses  
- 2024_False_Alarms  
- BATS-YTD  
- 2023-2024_OT  
- 2024_Responses  
- 2024_OT_Rank  
- BATS-Incidents  
- BATS-Activities  

### Public Works (PW)
- WORKORDER

### Police Department (PD)
- STAT_CEASEFIRE
- STAT_CFS
- STAT_CFS_HOMELESS
- STAT_CITATIONS
- STAT_COLLISION
- STAT_CRIME
- STAT_FIREARM
- STAT_SERVTIME_HOMELESS