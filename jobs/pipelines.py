import pg8000.native
import json
import logging
import os

class PostgresPipeline(object):
    # Init 
    user            =   "gelassenheit"
    password        =   "passwort"
    host            =   os.environ.get('DB_HOSTNAME', '')
    database        =   os.environ.get('DB_DATABASE', '')
    port            =   os.environ.get('DB_PORT', '')
    schema          =   os.environ.get('DB_SCHEMA', '')
    insert_table    =   os.environ.get('DB_INSERT_TABLE', '')
    
    def open_spider(self, spider):
        self.client = pg8000.connect(
                            user=self.user,
                            password = self.password,
                            host = self.host,
                            database = self.database,
                            port = self.port)
        self.curr = self.client.cursor()

    def close_spider(self, spider):
       self.client.close()

    def process_item(self, item, spider):
        # Create table to insert
        self.curr.execute("""
            CREATE TABLE IF NOT EXISTS {schema}.{insert_table} (
                job_title text,
                company text,
                job_description text,
                working_hours text,
                work_place text,
                type_of_employment text,
                company_size text,
                contact_person text,
                contact_person_email text,
                contact_person_phone text,
                contact_person_adress text,
                website text,
                crawl_ts text,
                PRIMARY KEY (job_title, crawl_ts)
            )
        """.format(schema=self.schema, insert_table=self.insert_table)
        )

        self.curr.execute("""
                        INSERT INTO {schema}.{insert_table} VALUES (
                                                                    '{job_title}', 
                                                                    '{company}',
                                                                    '{job_description}', 
                                                                    '{woring_hours}', 
                                                                    '{work_place}', 
                                                                    '{type_of_employment}', 
                                                                    '{company_size}', 
                                                                    '{contact_person}', 
                                                                    '{contact_person_email}', 
                                                                    '{contact_person_phone}', 
                                                                    '{contact_person_adress}',
                                                                    '{website}',
                                                                    '{crawl_ts}'
                                                                )
                        ON CONFLICT (job_title, crawl_ts)
                        DO UPDATE
                        SET 
                            company = excluded.company,
                            job_description = excluded.job_description,
                            working_hours = excluded.working_hours,
                            workplace = excluded.work_place,
                            type_of_employment = excluded.type_of_employment,
                            company_size = excluded.company_size,
                            contact_person = excluded.contact_person,
                            contact_person_email = excluded.contact_person_email,
                            contact_person_phone = excluded.contact_person_phone,
                            contact_person_adress = excluded.contact_person_adress,
                            website = excluded.website,
                        """.format(schema=self.schema, insert_table=self.insert_table, **item)
        )
        self.client.commit()
        logging.info("Upserted a record to the table '{schema}.{insert_table}'".format(schema=self.schema, insert_table=self.insert_table))
        return item
