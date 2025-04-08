from config.config_logging import setup_logging
from config.config import load_config
from helpers.sql_helpers import fetch_sql_data, connect_db
from helpers.az_helpers import upload_to_adls

# Set up logging and config
cfg = load_config()
logger = setup_logging()

if __name__ == "__main__":
    try:
        # Connect engines
        COS_ENGINE = connect_db(
            cfg.COS_DB_CREDS.DRIVER, 
            cfg.COS_DB_CREDS.SERVER, 
            cfg.COS_DB.OPDA_PROD, 
            cfg.COS_DB_CREDS.USERNAME, 
            cfg.COS_DB_CREDS.PASSWORD
        )

        COS_ENGINE_5 = connect_db(
            cfg.COS_DB_5_CREDS.DRIVER, 
            cfg.COS_DB_5_CREDS.SERVER, 
            cfg.COS_DB_5_CREDS.DB, 
            cfg.COS_DB_5_CREDS.USERNAME, 
            cfg.COS_DB_5_CREDS.PASSWORD
        )

        PD_ENGINE = connect_db(
            cfg.COS_DB_CREDS.DRIVER, 
            cfg.COS_DB_CREDS.SERVER, 
            cfg.COS_DB.PD, 
            cfg.COS_DB_CREDS.USERNAME, 
            cfg.COS_DB_CREDS.PASSWORD
        )

        # Define table names
        cdd_tables = [
            "accela_permit_cycles_prod", 
            "accela_resubmittal_cycles_prod",
            "accela_tasks_prod",
            "accela_department_cycles_prod"
        ]

        fire_tables = [
            "EventList",
            "Deep_Dive_TOT",
            "2024_Loss",
            "2023_Non_Homeless_Related",
            "2024_Non_Homeless_Related",
            "2023-2024_Homelessness",
            "2023_False_Alarms",
            "2023_Loss",
            "2023_Responses",
            "2024_False_Alarms",
            "BATS-YTD",
            "2023-2024_OT",
            "2024_Responses",
            "2024_OT_Rank",
            "BATS-Incidents",
            "BATS-Activities"
        ]

        pw_tables = [
            "WORKORDER"
        ]

        pd_tables = [
            "STAT_CEASEFIRE",
            "STAT_CFS",
            "STAT_CFS_HOMELESS",
            "STAT_CITATIONS",
            "STAT_COLLISION",
            "STAT_CRIME",
            "STAT_FIREARM",
            "STAT_SERVTIME_HOMELESS"
        ]

        # Define SQL queries
        query_cdd = f"SELECT * FROM [{cfg.COS_DB.OPDA_PROD}].[CDD].["
        query_fire = f"SELECT * FROM [{cfg.COS_DB.OPDA_PROD}].[FireSTAT].["
        query_pw = """
            SELECT [WORKORDERID],
                [DESCRIPTION],
                [STATUS], 
                [INITIATEDATE],
                [ACTUALFINISHDATE]    
            FROM [CWStocktonProd].[azteca].[WORKORDER]
            WHERE CAST(INITIATEDATE AS DATE) <= CAST(ACTUALFINISHDATE AS DATE)
            ORDER BY INITIATEDATE DESC;
        """
        query_pd = f"SELECT * FROM [{cfg.COS_DB.PD}].[dbo].["

        for table in cdd_tables:
            query = query_cdd + table + ']'
            cdd_blob_name = f"{table[:-4]}raw.parquet"
            cdd_df = fetch_sql_data(COS_ENGINE, query)

            # Upload to dev and prod
            upload_to_adls(cdd_df, cfg.AZ_CREDS.dev.CDD, cfg.AZ_CONT.dev.CDD, cdd_blob_name)
            upload_to_adls(cdd_df, cfg.AZ_CREDS.prod.CDD, cfg.AZ_CONT.prod.CDD, cdd_blob_name)

        for table in fire_tables:
            query = query_fire + table + ']'
            fire_blob_name = f"{table}_raw.parquet"
            fire_df = fetch_sql_data(COS_ENGINE, query)
            
            # Upload to dev and prod
            upload_to_adls(fire_df, cfg.AZ_CREDS.dev.FIRE, cfg.AZ_CONT.dev.FIRE, fire_blob_name)
            upload_to_adls(fire_df, cfg.AZ_CREDS.prod.FIRE, cfg.AZ_CONT.prod.FIRE, fire_blob_name)

        for table in pw_tables:
            pw_blob_name = f"{table}_raw.parquet"
            pw_df = fetch_sql_data(COS_ENGINE_5, query_pw)
            
            # Upload to dev and prod
            upload_to_adls(pw_df, cfg.AZ_CREDS.dev.PW, cfg.AZ_CONT.dev.PW, pw_blob_name)
            upload_to_adls(pw_df, cfg.AZ_CREDS.prod.PW, cfg.AZ_CONT.prod.PW, pw_blob_name)

        for table in pd_tables:
            query = query_pd + table + ']'
            pd_blob_name = f"{table}_raw.parquet"
            pd_df = fetch_sql_data(PD_ENGINE, query)
            
            # Upload to dev and prod
            upload_to_adls(pd_df, cfg.AZ_CREDS.dev.PD, cfg.AZ_CONT.dev.PD, pd_blob_name)
            upload_to_adls(pd_df, cfg.AZ_CREDS.prod.PD, cfg.AZ_CONT.prod.PD, pd_blob_name)

    finally:
        COS_ENGINE.dispose()
        logger.info(f'Connection closed to {COS_ENGINE}, pipeline complete')

        COS_ENGINE_5.dispose()
        logger.info(f'Connection closed to {COS_ENGINE_5}, pipeline complete')

        PD_ENGINE.dispose()
        logger.info(f'Connection closed to {PD_ENGINE}, pipeline complete')