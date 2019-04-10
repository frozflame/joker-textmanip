Changes of joker-textmanip
==========================

#### 0.2.1
add `jt.tabular.text{,file}_{to_list,to_dict,numsum}`

#### 0.2.0
* explode `jt.parse` into `jt.{url,tabular,useragent}`
* add `jt.cjk.who_can_{en,de}code()`
* add `jt.path.make_new_path()`
* add `jt.stream.{iter_lines,nonblank_lines_of}`

#### 0.1.0
* remove modules: `jt.misc`, `jt.draw`, `jt.uniblk`
* rename `jt.chinese` to `jt.cjk`
* add module `jt.data` and `asset` directory for builtin datasets
* add `jt.regex.make_range_pattern()`
* add `jt.cjk.remove_cjk()`,  `jt.cjk.remove_spaces_be{side,tween}_cjk`
* add `jt.cjk.brutal_cjk_decode()`
* add `remove_emptylines()`, `dedup_spaces()`, `proper_join()` in `jt.__init__`
* add `jt.path.adapt_outpath()`
* add `jt.parse.url.validate_ipv{4,6}_address()`

#### 0.0.6
* move random_string(), b64_chars, etc to `textmanip.__init__`
* add functions `j.tm.remove_*`
* add functions `j.tm.path.*_filename_safe`

#### 0.0.5
* add functions find_common_prefix, find_common_suffix

#### 0.0.4
* add function url_simplify

#### 0.0.3
* remove .filepath
* remove .parse.url.validate_ipv?_address
* add joker-cast to requirements.txt

#### 0.0.2
* new function: .draw.make_title_box()
