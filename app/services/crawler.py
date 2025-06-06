from crawl4ai import AsyncWebCrawler


class WebsiteCrawler:
    async def crawl_website(self, url: str):
        """Extracts main content using Azure OpenAI with updated crawl4ai API"""
        try:
            print(f"Starting to crawl: {url}")
            async with AsyncWebCrawler(verbose=True) as crawler:
                result = await crawler.arun(url=url)
                print(f"Extraction result: {result.markdown[:300]}")
                if not result or not result.markdown:
                    raise Exception("No content extracted from the page")

                print(f"Successfully extracted content from {url}")
                return result.markdown

        except Exception as e:
            print(f"Error crawling {url}: {str(e)}")
            raise Exception(f"Failed to crawl website: {str(e)}")