############   NATIVE IMPORTS  ###########################
from typing import List
############ INSTALLED IMPORTS ###########################
############   LOCAL IMPORTS   ###########################
##########################################################
def keyword_filter_dropdown(keywords:List[str]) -> str:
    return f"""
    <div id="search_by_keyword" style = "font-size:10px;text-align:center;font-family:Arial, Helvetica, sans-serif">
    <input type="text" placeholder="Search.." id="keyword" onkeyup="filterFunction()">
    <br>
    """ + "\n".join(
        map(
            lambda keyword:f'<a style="text-decoration: none; display:none" href = /search/{keyword}>{keyword}</a>',
            keywords
        )
    ) + """
    </div>

    <script>
        function filterFunction() {
          var input, filter, ul, li, a, i;
          input = document.getElementById("keyword");
          filter = input.value.toUpperCase();
          div = document.getElementById("search_by_keyword");
          a = div.getElementsByTagName("a");
          for (i = 0; i < a.length; i++) {
            txtValue = a[i].textContent || a[i].innerText;
            if (txtValue.toUpperCase().indexOf(filter) > -1) {
              a[i].style.display = "";
            } else {
              a[i].style.display = "none";
            }
          }
        }
    </script>
    """

def list_options_html(options:List[str], urls:List[str],selected_option:str) -> str:
    SELECTED = 'selected="selected"'
    return '\n'.join(
        map(
            lambda option,url:f'<option {SELECTED if option == selected_option else ""} value="{url}">{option}</option>',
            options,
            urls
        )
    ) + """
    <script>
    jQuery(function($) {
        $('#search_chapter_name, #search_chapter_number, #search_verse_number').on('change', function() {
            var url = $(this).val();
            if (url) {
                window.location = url;
            }
            return false;
        });
    });
    </script>
    """

def format_sentences_to_be_hidden_html(sentences:List[str],default_displayed:int) -> str:
    indexes = range(len(sentences))
    HIDE = 'none'
    SHOW = 'block'
    hide = "hide"
    show = "show"
    SELECTED = 'selected="selected"'
    UNSELECTED = ''
    return '<div style = "text-align:center;font-family:Arial, Helvetica, sans-serif" class="parallel-english-translations-of-verse">' + '<select id="translator" style="background-color:lightgoldenrodyellow;border-top:none;border-left:none;border-right:none">' + '\n'.join(
        map(
            lambda index: f'<option {(UNSELECTED,SELECTED)[index==default_displayed]} value="{index}">English Translation {index}</option>',
            indexes
        )
    ) + '</select><br><br>' + '\n'.join(
        map(
            lambda index,sentence:f'<div id="translation{index}" style="display:{(HIDE,SHOW)[index==default_displayed]}"><small>{format_sentence_for_html(sentence)}</small></div>',
            indexes,
            sentences
        )
    ) +  "</div>" + "<script>$('#translator').on('change', function () {" + '\n'.join(
            map(
                lambda selected_index:f'if( $(this).val()==="{selected_index}")' + "{" + '\n'.join(
                    map(
                        lambda index: f'$("#translation{index}").{(hide,show)[selected_index==index]}()',
                        indexes
                    ) 
                ) + "}",
                indexes
            )
        ) + "});</script>"
    
def format_and_link_verses_for_html(button_text:str,verses:List[str],verses_to_display:List[str],scripture:str) -> str:
    return f"""<div class="dropdown"  style = "font-size: 10px;text-align:center;font-family:Arial, Helvetica, sans-serif">
        <button onclick="toggleDisplay{scripture}()" style="background-color:lightgoldenrodyellow;border-top:none;border-left:none;border-right:none">{button_text}</button>
    </div>

    <div id="drop_down_menu_{scripture}" style="display:none">   
    """ + ' '.join(  
        "<p><small><a href= /{scripture}/{verse_address}>{verse}</a>  {verse_to_display}...</small></p>".format(
            scripture=scripture,
            verse_address=verse.replace(':','/'),
            verse=verse.replace('%20',' '),
            verse_to_display=text,
        ) for verse,text in zip(verses,verses_to_display)
    ) + f"""
    </div>

    <script>
        function toggleDisplay{scripture}()""" +  "{" + f"""
            var x = document.getElementById("drop_down_menu_{scripture}");
            if (x.style.display === "none") """ + """{
                x.style.display = "block";
            } else {
                x.style.display = "none";
            }
        }
    </script>

    """

def format_sentence_for_html(sentence:str) -> str:
    return sentence.replace(",",",<br>").replace(";",";<br>").replace(
        ":",":<br>").replace("-","-<br>").replace("—","—<br>").replace(
        ".",".<br><br>").replace("!","!<br><br>").replace("?","?<br><br>")