-- Lua filter for Pandoc: replace longtable with tabular in a table float
-- Required for twocolumn LaTeX modes where longtable is incompatible

local function escape_str(s)
  s = s:gsub("%%", "\\%%")
  s = s:gsub("&", "\\&")
  s = s:gsub("#", "\\#")
  s = s:gsub("_", "\\_")
  return s
end

local function inlines_to_latex(inlines)
  local result = {}
  for _, inline in ipairs(inlines) do
    if inline.t == "Str" then
      table.insert(result, escape_str(inline.text))
    elseif inline.t == "Space" then
      table.insert(result, " ")
    elseif inline.t == "Strong" then
      table.insert(result, "\\textbf{" .. inlines_to_latex(inline.content) .. "}")
    elseif inline.t == "Emph" then
      table.insert(result, "\\textit{" .. inlines_to_latex(inline.content) .. "}")
    elseif inline.t == "Code" then
      table.insert(result, "\\texttt{" .. escape_str(inline.text) .. "}")
    elseif inline.t == "Math" then
      if inline.mathtype == "InlineMath" then
        table.insert(result, "$" .. inline.text .. "$")
      else
        table.insert(result, "$$" .. inline.text .. "$$")
      end
    elseif inline.t == "RawInline" and inline.format == "tex" then
      table.insert(result, inline.text)
    elseif inline.t == "SoftBreak" or inline.t == "LineBreak" then
      table.insert(result, " ")
    elseif inline.t == "Subscript" then
      table.insert(result, "\\textsubscript{" .. inlines_to_latex(inline.content) .. "}")
    elseif inline.t == "Superscript" then
      table.insert(result, "\\textsuperscript{" .. inlines_to_latex(inline.content) .. "}")
    else
      table.insert(result, pandoc.utils.stringify(inline))
    end
  end
  return table.concat(result)
end

local function blocks_to_latex(blocks)
  local parts = {}
  for _, block in ipairs(blocks) do
    if block.t == "Para" or block.t == "Plain" then
      table.insert(parts, inlines_to_latex(block.content))
    else
      table.insert(parts, pandoc.utils.stringify(block))
    end
  end
  return table.concat(parts, " ")
end

function Table(tbl)
  local ncols = #tbl.colspecs
  local aligns = {}
  for _, spec in ipairs(tbl.colspecs) do
    local a = spec[1]
    if a == pandoc.AlignLeft or a == pandoc.AlignDefault then
      table.insert(aligns, "l")
    elseif a == pandoc.AlignRight then
      table.insert(aligns, "r")
    elseif a == pandoc.AlignCenter then
      table.insert(aligns, "c")
    else
      table.insert(aligns, "l")
    end
  end

  local lines = {}
  table.insert(lines, "\\begin{table}[htbp]")
  table.insert(lines, "\\centering")
  table.insert(lines, "\\small")
  table.insert(lines, "\\begin{tabular}{" .. table.concat(aligns) .. "}")
  table.insert(lines, "\\toprule")

  -- Header
  if tbl.head and tbl.head.rows then
    for _, row in ipairs(tbl.head.rows) do
      local cells = {}
      for _, cell in ipairs(row.cells) do
        table.insert(cells, "\\textbf{" .. blocks_to_latex(cell.contents) .. "}")
      end
      table.insert(lines, table.concat(cells, " & ") .. " \\\\")
    end
    table.insert(lines, "\\midrule")
  end

  -- Body
  for _, body in ipairs(tbl.bodies) do
    for _, row in ipairs(body.body) do
      local cells = {}
      for _, cell in ipairs(row.cells) do
        table.insert(cells, blocks_to_latex(cell.contents))
      end
      table.insert(lines, table.concat(cells, " & ") .. " \\\\")
    end
  end

  table.insert(lines, "\\bottomrule")
  table.insert(lines, "\\end{tabular}")
  table.insert(lines, "\\end{table}")

  return pandoc.RawBlock("latex", table.concat(lines, "\n"))
end
