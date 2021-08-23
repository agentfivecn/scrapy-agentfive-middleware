from scrapy import signals
from scrapy.spiders import Spider
from scrapy.utils.reqser import request_from_dict, request_to_dict

import urllib.parse as urlparse
from urllib.parse import urlencode

import logging
logger = logging.getLogger("agentfive-middleware")

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter

META_KEY = "agentfive"

class AgentfiveMiddleware:
    url = "https://api.agentfive.cn/v1"
    apikey = ""
    enabled = False

    @classmethod
    def from_crawler(cls, crawler):
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s
    
    def _read_settings(self, spider: Spider) -> None:
        settings = spider.crawler.settings
        if not settings.get("AGENTFIVE_KEY"):
            self.enabled = False
            logger.info("agentfive API cannot be used without an apikey")
            return

        self.apikey = settings["AGENTFIVE_KEY"]

        if settings.get("AGENTFIVE_API_URL"):
            self.url = settings["AGENTFIVE_API_URL"]

        self.raise_on_error = settings.getbool("AGENTFIVE_RAISE_ON_ERROR", True)

        self.default_args = settings.getdict("AGENTFIVE_DEFAULT_ARGS", {})

    def _full_url(self, query_params):
        url_parts = list(urlparse.urlparse(self.url))
        query = dict(urlparse.parse_qsl(url_parts[4]))
        query.update(query_params)

        url_parts[4] = urlencode(query)
        return urlparse.urlunparse(url_parts)

    def process_request(self, request, spider):
        if not self.enabled:
            return None
        
        try:
            agentfive_meta = request.meta[META_KEY]
        except KeyError:
            agentfive_meta = {}

        if agentfive_meta.get("skip") or agentfive_meta.get("original_request"):
            return None
        
        params = agentfive_meta.copy()
        try:
            del params["skip"]
        except KeyError:
            pass

        params.update({"url": request.url, "key": self.apikey})

        additional_meta = {
            "original_request": request_to_dict(request, spider=spider),
        }
        agentfive_meta.update(additional_meta)

        request.meta[META_KEY] = agentfive_meta
        return request.replace(url=self._full_url(params))


    def process_response(self, request, response, spider):
        if not self.enabled:
            return response

        try:
            agentfive_meta = request.meta[META_KEY]
        except KeyError:
            agentfive_meta = {}

        if agentfive_meta.get("skip") or not agentfive_meta.get("original_request"):
            return response

        original_request = request_from_dict(agentfive_meta["original_request"], spider=spider)

        return response.replace(url=original_request.url)

    def spider_opened(self, spider):
        self.enabled = True
        self._read_settings(spider)
        if self.enabled:
            logger.info("Using agentfive API at %s with apikey %s***" % (self.url, self.apikey[:5]))
