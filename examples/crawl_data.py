from src.pipelines.crawl import CrawlPipeline


crawl_pipe = CrawlPipeline()
card_infos = crawl_pipe.crawl_from_json_file("assets/maliss.json")
crawl_pipe.save_crawl_data(card_infos, "raw_data/Maliss")