from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
from datetime import datetime, timedelta
import time
import os
import subprocess
import logging

def set_logging(): 
    # Get current time and convert to date
    today = datetime.now().strftime("%Y-%m-%d")
    #log_file = f'jobs/logs/{today}.log'
    log_dir = "jobs/logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, f"{today}.log")
    # Create an empty log file if not exist
    if not os.path.exists(log_file):
        open(log_file, 'a')
    else:
        pass
    # Set logging config
    logging.basicConfig(filename=log_file, 
                        encoding='utf-8', 
                        level=logging.INFO, 
                        filemode='a', 
                        format='%(levelname)s: %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S')


def run_spider(): 
        set_logging()
        # Start 
        logging.info('Started crawling {}...'.format(datetime.now()))
        # Run scrapy crawl
        print('Logging Started...')
        subprocess.run(['scrapy', 'crawl', 'test'])
        # End
        logging.info('Finished crawling {}...'.format(datetime.now()))

def asyncio_schedule():
    """schedule tasks"""
    def run_spider(): 
        set_logging()
        # Start 
        logging.info('Started crawling {}...'.format(datetime.now()))
        # Run scrapy crawl
        subprocess.run(['scrapy', 'crawl', 'test'])
        # End
        logging.info('Finished crawling {}...'.format(datetime.now()))


    def remove_old_log():
        # Delete logs older than 21 days
        date_delete = (datetime.now() - timedelta(days=21)).strftime("%Y-%m-%d")
        log_dir = "jobs/logs"
        log_delete = os.path.join(log_dir, f"{date_delete}.log")
        try:
            os.remove(log_delete)
        except Exception as msg:
            logging.info(f"log '{log_delete}' doesn't exist, skip delete log file!")
        else:
            logging.info(f"deleted {log_delete}!")

    scheduler = AsyncIOScheduler()
    # Add task to crawl per hour between 7a.m to 7p.m
    scheduler.add_job(func=run_spider, trigger='cron', hour='6')
    # Add task to clean old log, keep logs for last 14 days only, run at 11:30p.m
    scheduler.add_job(func=remove_old_log, trigger='cron', hour='23', minute='30')
    # Start process
    scheduler.start()
    print('Press Ctrl+C to exit')

    # Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
    try:
        asyncio.get_event_loop().run_forever()
    except (KeyboardInterrupt, SystemExit):
        pass 
        
if __name__ == '__main__':
    # Running message
    print('Started application {}'.format(datetime.now()))
    print('****************************** APP IS RUNNING ******************************')
    # Run process
    #asyncio_schedule()
    run_spider()
    