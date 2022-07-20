require('plugins')

vim.cmd [[
:set number
:set relativenumber
:set mouse=a
]]

if vim.g.nvui then
  -- Configure through vim commands
  vim.cmd [[NvuiCmdFontFamily MeslaLGS NF]]
end 

vim.cmd [[
call plug#begin()
Plug 'nanotee/sqls.nvim'

" For vsnip users.
Plug 'hrsh7th/cmp-vsnip'
Plug 'hrsh7th/vim-vsnip'

Plug 'ncm2/ncm2'
Plug 'SirVer/ultisnips'
Plug 'honza/vim-snippets'

Plug 'vimwiki/vimwiki'

Plug 'kyazdani42/nvim-web-devicons' " optional, for file icons
Plug 'kyazdani42/nvim-tree.lua'

Plug 'tpope/vim-fugitive'

Plug 'sheerun/vim-polyglot'

Plug 'preservim/nerdtree'

Plug 'windwp/nvim-autopairs'

Plug 'vim-airline/vim-airline'
Plug 'vim-airline/vim-airline-themes'

Plug 'BurntSushi/ripgrep'
Plug 'sharkdp/fd'
Plug 'nvim-telescope/telescope-fzf-native.nvim', { 'do': 'cmake -S. -Bbuild -DCMAKE_BUILD_TYPE=Release && cmake --build build --config Release && cmake --install build --prefix build' }
Plug 'nvim-treesitter/nvim-treesitter'
Plug 'kyazdani42/nvim-web-devicons'
Plug 'nvim-lua/plenary.nvim'
Plug 'nvim-telescope/telescope.nvim', { 'tag': '0.1.0' }

" Cosmic UI
Plug 'MunifTanjim/nui.nvim'
Plug 'CosmicNvim/cosmic-ui'
call plug#end()
]]

--require'lspconfig'.pyright.setup{}
--require'lspconfig'.serve_d.setup{}

require("nvim-autopairs").setup {}
require("nvim-tree").setup()

require('lspconfig').sqls.setup{
    on_attach = function(client, bufnr)
        require('sqls').on_attach(client, bufnr)
    end
}

require('cosmic-ui').setup()

vim.cmd [[
" Vimwiki toggle list items
nnoremap <leader>t :VimwikiToggleListItem<CR>
" NVim Tree
nnoremap <leader>b :NvimTreeOpen<CR>

" Using Lua functions
nnoremap <leader>ff <cmd>lua require('telescope.builtin').find_files()<cr>
nnoremap <leader>fg <cmd>lua require('telescope.builtin').live_grep()<cr>
nnoremap <leader>fb <cmd>lua require('telescope.builtin').buffers()<cr>
nnoremap <leader>fh <cmd>lua require('telescope.builtin').help_tags()<cr>
]]


-- soft tabs
vim.cmd [[
set tabstop=2
set softtabstop=2
set shiftwidth=2
set expandtab
]]

-- vim-airline config
vim.cmd [[
let g:airline_powerline_fonts = 1
let g:airline_theme='jellybeans'
]]

-- AUTO COMPLETION
vim.cmd [[
set completeopt=menu,menuone,noselect
]]

local cmp = require'cmp'

  cmp.setup({
    snippet = {
      -- REQUIRED - you must specify a snippet engine
      expand = function(args)
        vim.fn["vsnip#anonymous"](args.body) -- For `vsnip` users.
        -- require('luasnip').lsp_expand(args.body) -- For `luasnip` users.
        -- require('snippy').expand_snippet(args.body) -- For `snippy` users.
        -- vim.fn["UltiSnips#Anon"](args.body) -- For `ultisnips` users.
      end,
    },
    window = {
      -- completion = cmp.config.window.bordered(),
      -- documentation = cmp.config.window.bordered(),
    },
    mapping = cmp.mapping.preset.insert({
      ['<C-b>'] = cmp.mapping.scroll_docs(-4),
      ['<C-f>'] = cmp.mapping.scroll_docs(4),
      ['<C-Space>'] = cmp.mapping.complete(),
      ['<C-e>'] = cmp.mapping.abort(),
      ['<CR>'] = cmp.mapping.confirm({ select = true }), -- Accept currently selected item. Set `select` to `false` to only confirm explicitly selected items.
    }),
    sources = cmp.config.sources({
      { name = 'nvim_lsp' },
      { name = 'vsnip' }, -- For vsnip users.
      -- { name = 'luasnip' }, -- For luasnip users.
      -- { name = 'ultisnips' }, -- For ultisnips users.
      -- { name = 'snippy' }, -- For snippy users.
    }, {
      { name = 'buffer' },
    })
  })

  -- Set configuration for specific filetype.
  cmp.setup.filetype('gitcommit', {
    sources = cmp.config.sources({
      { name = 'cmp_git' }, -- You can specify the `cmp_git` source if you were installed it.
    }, {
      { name = 'buffer' },
    })
  })

  -- Use buffer source for `/` (if you enabled `native_menu`, this won't work anymore).
  cmp.setup.cmdline('/', {
    mapping = cmp.mapping.preset.cmdline(),
    sources = {
      { name = 'buffer' }
    }
  })

  -- Use cmdline & path source for ':' (if you enabled `native_menu`, this won't work anymore).
  cmp.setup.cmdline(':', {
    mapping = cmp.mapping.preset.cmdline(),
    sources = cmp.config.sources({
      { name = 'path' }
    }, {
      { name = 'cmdline' }
    })
  })

  -- Setup lspconfig.
  local capabilities = require('cmp_nvim_lsp').update_capabilities(vim.lsp.protocol.make_client_capabilities())
  -- Replace <YOUR_LSP_SERVER> with each lsp server you've enabled.
  require('lspconfig')['serve_d'].setup {
    capabilities = capabilities
  }

  require('lspconfig').sqls.setup{
    on_attach = function(client, bufnr)
        require('sqls').on_attach(client, bufnr)
    end
  }
