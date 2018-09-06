The server implemented in `texserver.lua` listens on port `8080` and waits for
`POST` requests with JSON data in the following format:

    {"command":"lualatex filename.tex", "dir":"path/to/dir/with/filename.tex"}

The server depends on [lua-http](https://github.com/daurnimator/lua-http), it
must be executed using stock Lua instead of `texlua`.

Example client is in `texclient.lua`.

It is meant for usage in Docker images, the directory with TeX files should be
mounted using volumes, it is also good idea to filter the network access, there
is no authentication for commands executed. It shouldn't be executed outside
sandbox.
