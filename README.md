This package provides a Scrapy
[Downloader Middleware](https://docs.scrapy.org/en/latest/topics/downloader-middleware.html)
to interact with the
[agentfive API](https://www.agentfive.cn/documents).

## Requirements

* Python 3.5+
* Scrapy 1.6+

## Installation

`pip install scrapy-agentfive-middleware`

## Configuration

Enable the `AgentfiveMiddleware` via the
[`DOWNLOADER_MIDDLEWARES`](https://docs.scrapy.org/en/latest/topics/settings.html#downloader-middlewares)
setting:

```
DOWNLOADER_MIDDLEWARES = {
    "agentfive_middleware.AgentfiveMiddleware": 585,
}
```

Please note that the middleware needs to be placed before the built-in `HttpCompressionMiddleware`
middleware (which has a priority of 590), otherwise incoming responses will be compressed and the
agentfive middleware won't be able to handle them.

### Settings

* `AGENTFIVE_KEY` (type `str`)

    API key to be used to authenticate against the agentfive API.

* `AGENTFIVE_API_URL` (Type `str`, default `"https://api.agentfive.cn/v1"`)

    The endpoint of a agentfive API.

* `AGENTFIVE_DEFAULT_ARGS` (type `dict`, default `{}`)

    Default values to be sent to the agentfive API. For instance, set to `{"profile": "mobile"}`
    to set all requests with a mobile profile.

## Usage

If the middleware is enabled, by default all requests will be redirected to the specified
agentfive API endpoint, and append necessary params which agentfive API expected. 

For example:

```python
scrapy.Request(url="https://httpbin.org/anything")
```

will be set to agentfive API and let agentfive to fetch the url.

### Additional arguments

Additional arguments could be specified under the `agentfive` `Request.meta` key. For instance:

```python
Request(
    url="https://example.org",
    meta={"crawlera_fetch": {"render": True, "wait_ms": 5000}},
)
```

for more information on agentfive API parameter, please refer to [agentfive document](https://www.agentfive.cn/documents).

### Skipping requests

You can instruct the middleware to skip a specific request by setting the `agentfive.skip`
[Request.meta](https://docs.scrapy.org/en/latest/topics/request-response.html#scrapy.http.Request.meta)
key:

```python
Request(
    url="https://example.org",
    meta={"agentfive": {"skip": True}},
)
```
