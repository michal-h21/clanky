local http_server = require "http.server"
local http_headers = require "http.headers"
local lfs = require "lfs"
local os = require "os"
local io = require "io"
local json = require "json"

local function get_command(stream)
  local data = stream:get_body_as_string()
  print("data: ", data)
  if not data then return nil, "No data" end
  local fields = json.decode(data)
  return fields
end

local function run_command(command)
  local cmd = command.command
  local dir = command.dir
  if not cmd or not dir then
    return nil, "No command or dir"
  end
  lfs.chdir(dir)
  local runner = io.popen(cmd, "r")
  local response = runner:read("all")
  runner:close()
  if response then
    print(string.format("Command %s in dir %s ran correctly", cmd, dir))
  end
  return response, ""
end




local function reply(myserver, stream) -- luacheck: ignore 212
	-- Read in headers
	local req_headers = assert(stream:get_headers())
	local req_method = req_headers:get ":method"

	-- Log request to stdout
	assert(io.stdout:write(string.format('[%s] "%s %s HTTP/%g"  "%s" "%s"\n',
		os.date("%d/%b/%Y:%H:%M:%S %z"),
		req_method or "",
		req_headers:get(":path") or "",
		stream.connection.version,
		req_headers:get("referer") or "-",
		req_headers:get("user-agent") or "-"
	)))
  local command, msg = get_command(stream)

  local res_headers = http_headers.new()
  if not command then
    res_headers:append(":status", "303")
    print("Command failed: ".. msg)
    print("Stream: " .. stream:get_body_as_string())
    return nil
  end
  local response = run_command(command)
	-- Build response headers
  res_headers:append(":status", "200")
	res_headers:append("content-type", "text/plain")
	-- Send headers to client; end the stream immediately if this was a HEAD request
	assert(stream:write_headers(res_headers, req_method == "HEAD"))
	if req_method ~= "HEAD" then
		-- Send body, ending the stream
		assert(stream:write_chunk(response, true))
	end
end

local myserver = assert(http_server.listen {
	host = "localhost";
	port = 8080;
	onstream = reply;
	onerror = function(myserver, context, op, err, errno) -- luacheck: ignore 212
		local msg = op .. " on " .. tostring(context) .. " failed"
		if err then
			msg = msg .. ": " .. tostring(err)
		end
		assert(io.stderr:write(msg, "\n"))
	end;
})

-- Manually call :listen() so that we are bound before calling :localname()
assert(myserver:listen())
do
	local bound_port = select(3, myserver:localname())
	assert(io.stderr:write(string.format("Now listening on port %d\n", bound_port)))
end
-- Start the main server loop
assert(myserver:loop())
