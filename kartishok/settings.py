BOT_NAME = 'kartishok'
SPIDER_MODULES = ['kartishok.spiders']
NEWSPIDER_MODULE = 'kartishok.spiders'
ROBOTSTXT_OBEY = True
LOG_LEVEL = 'WARNING'
ITEM_PIPELINES = {
   'kartishok.pipelines.DatabasePipeline': 300,
}
