local dir_name = [==[полный путь до папки с постами]==]

-- case sensitive!
local words = {
    { 'слово один', 'или два' },
    'и три',
}

local function predicate(text)
    for _, w in ipairs(words) do
        local found = false
        if type(w) == 'table' then
            for _, ww in ipairs(w) do
                if string.find(text, ww) then
                    found = true
                    break
                end
            end
        else
            found = string.find(text, w) ~= nil
        end
        if not found then return false end
    end
    return true
end

local prev_texts = {}
local cur = 0
local sd = vim.loop.fs_scandir(dir_name)

local function searchNext()
    while true do
        local filename, ftype = vim.loop.fs_scandir_next(sd)
        if filename == nil then
            return true
        elseif ftype == 'file' then
            local file = io.open(dir_name .. '\\' .. filename, 'r')
            if file == nil then
                return 'Error for ' .. filename .. '!'
            end
            local text = file:read('*a')
            file:close()
            if predicate(text) then
                local lines = vim.split(text, '\n')
                table.insert(lines, 1, filename)
                return lines
            end
        end
    end
end

local function goNext()
    local next
    if prev_texts[cur] == true then
        next = true
    elseif cur < #prev_texts then
        cur = cur + 1
        next = prev_texts[cur]
    else
        next = searchNext()
        cur = cur + 1
        table.insert(prev_texts, next)
        print(next)
    end

    if next == true then
        next = { 'Done!' }
    end
    vim.api.nvim_buf_set_lines(0, 0, -1, false, next)
    print('Now at #' .. cur)
end

local function goPrev()
    local next
    if cur > 0 then
        cur = cur - 1
        next = prev_texts[cur]
    end
    if not next then
        next = { 'Start!' }
    end
    vim.api.nvim_buf_set_lines(0, 0, -1, false, next)
    print('Now at #' .. cur)
end

-- numpad 4 и 6 переносят к предыдущему и следующему файлу
-- с совпадением
vim.keymap.set('n', '<k4>', goPrev)
vim.keymap.set('n', '<k6>', goNext)
