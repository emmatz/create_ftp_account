set nocompatible    " Recomended by https://engineering.purdue.edu/ece264/16au/static/.vimrc.html

syntax on               " Turn on syntax highlightied.
set history=10000       " Keep XX lines of command line history
set paste               " Compatible for copying and paste.
set number              " Add number line
set foldmethod=syntax   " Fold methods indent, syntax, manual, marker, expr, diff
set hlsearch            " Highligth occurrences of a word
"set laststatus=2        " (ls) Shows status line always
"set relativenumber      " (rnu) Shows relative up and down lines number
set ruler               " Show the cursor position all the time
set rulerformat=%l\ col:%v\ (%p%%)\ %L
"set rulerformat=%15(%l,%c%V\ %p%%%)  " Line, column and percentage of file


function! UseSpaces()   " https://stackoverflow.com/questions/1878974/redefine-tab-as-4-spaces
    set tabstop=4       " (ts) Size of a hard tabstop.
    set shiftwidth=4    " (sw) Size of an indentation
    set softtabstop=4   " (sts) Number of spaces a <Tab> counts for. When 0, featuer is off.
    set smarttab        " Inserts blanks on a <Tab> key (as per sw, ts and sts).
    set expandtab       " (et) Use space caharacters, never tab characters.
    set autoindent      " (ai) Copy indent from current line when starting a new line.
endfunction

function! UseTabs()
    set tabstop=4     " (ts) Size of a hard tabstop.
    set shiftwidth=4  " (sw) Size of an indentation.
    set noexpandtab   " (noet) Always uses tabs instead of space characters.
    set autoindent    " (ai) Copy indent from current line when starting a new line.
endfunction


" Plugins section - curl -fLo ~/.vim/autoload/plug.vim --create-dirs     https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
call plug#begin('~/.vim/plugged')   " Activates vim-plug

Plug 'Yggdroot/indentLine'          " Install indent lines

call plug#end()
" End plugin section

:call UseSpaces()   " Default function
