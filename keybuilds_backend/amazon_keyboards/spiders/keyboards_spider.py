import os
import scrapy
import json


class KeyboardListSpider(scrapy.Spider):
    name = "keyboardsList"

    def start_requests(self):
        for i in range(3):
            page_index = i + 1
            url = f"https://www.amazon.com/s?k=mechanical+keyboard&page={page_index}"
            yield scrapy.Request(
                url=url, callback=self.parse, meta={"index": page_index}
            )

    def parse(self, response):
        # data_index = f"data-index='{response.meta['index']}'"
        data_component_type = "data-component-type=s-search-result"
        class_result_item = ".s-result-item"

        yield {
            f"page{response.meta['index']}": response.css(
                f"div[{data_component_type}]{class_result_item} a::attr(href)"
            ).getall()
        }


class KeyboardsSpider(scrapy.Spider):
    name = "keyboards"

    def start_requests(self):
        urls = []

        with open("keyboardsList.json", "r") as f:
            data = json.load(f)

        # print("---------")
        # print(f"list directory: {os.listdir()}")
        # print("---------")

        for url_list in data:
            print("------")
            print(url_list)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        yield {
            "title": response.css("title::text").get(),
            "price": response.css(".a-offscreen::text").get(),
        }
