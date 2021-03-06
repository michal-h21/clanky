local domobject = require "luaxml-domobject"

local functions = {
  p = function(x)
    context(x)
    context.par()
  end,
  ul = function(x)
    context.startitemize()
    context(x)
    context.stopitemize()
  end,
  ol = function(x)
    context.startitemize({"n"})
    context(x)
    context.stopitemize()
  end,
  li = function(x)
    context.startitem()
    context(x)
    context.stopitem()
    -- context.item(x)
  end,
  br = function()
    context.crlf()
  end,
  h1 = function(x)
    context.par()
    context.blank({"big"})
    context.bgroup()
    context.tfc()
    context.bold(x)
    context.egroup()
    context.blank({"small"})
    context.par()
  end,
  h2 = function(x)
    context.par()
    context.blank({"big"})
    context.bgroup()
    context.tfb()
    context.bold(x)
    context.egroup()
    context.blank({"small"})
    context.par()
  end,
  h3 = function(x)
    context.par()
    context.blank({"big"})
    context.bgroup()
    context.bold(x)
    context.egroup()
    context.blank({"small"})
    context.par()
  end,
  table = function(x)
    print("table", x)
    context.bTABLE({split="yes"})
    -- proč je nutné použít x()?
    context(x())
    context.eTABLE()
  end,
  tr = function(x)
    print("tr", x)
    context.bTR()
    context(x())
    context.eTR()
  end,
  th = function(x)
    print("th", x)
    context.bTD()
    context(x())
    context.eTD()
  end,
  td = function(x)
    print("td", x)
    context.bTD()
    context(x)
    context.eTD()
  end,
  thead = function(x)
    context(x())
  end,
  tbody = function(x)
    context(x())
  end,
  b = function(x)
    context.bold(x)
  end,
  i = function(x)
    context.italic(x)
  end,
  em = function(x)
    context.italic(x)
  end,
  strong = function(x)
    context.bold(x)
  end,
  div = function(x)
    context(x())
  end,
  tt = function(x)
    context.bgroup()
    context.tt(x)
    context.egroup()
  end,
  code = function(x)
    context.bgroup()
    context.tt(x)
    context.egroup()
  end,
  img = function(x, el)
    local url = el:get_attribute("src")
    context.externalfigure {url}
  end,
  pre = function(x, el)
    -- don't process contents of the pre element, just get the text
    local content = el:get_text()
    buffers.assign("pre", content)
    context.typebuffer {"pre"}
  end,
  article = function(x)
    context(x())
  end,
  a = function(x, el)
    local url = el:get_attribute("href")
    context(x)
    context.footnote(url)
    -- context.footnote(url)
  end
}


function process_children(el, cssobj)
  -- local style = cssobj
  -- ToDo: set the following functions according to the CSS
  local current_function = functions[el._name] or context
  
  local text_style = function(t)
    t = t:gsub("^%s+", " "):gsub("%s+$", " ")
    t = t:gsub("\\", "\\textbackslash{}")
    context(t)
  end
  current_function(function()
    for _, child in ipairs(el:get_children()) do
      if child:is_text() then
        text_style(child:get_text())
      elseif child:is_element() then
        process_children(child, cssobj)
      end
    end
  end,
  el, cssobj
  )
end

local function process(content,cssobj)
  local dom = domobject.parse(content)
  local body = dom:query_selector("body")[1]
  process_children(body,cssobj)
end

local M = {}

M.process = process
return M
