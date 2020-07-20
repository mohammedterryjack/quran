############   NATIVE IMPORTS  ###########################
from typing import List
############ INSTALLED IMPORTS ###########################
############   LOCAL IMPORTS   ###########################
##########################################################
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
    return '<div style = "text-align:center;font-family:Arial, Helvetica, sans-serif" class="parallel-english-translations-of-verse">' + '\n'.join(
        map(
            lambda index,sentence:f'<div id="translation{index}" style="display:{(HIDE,SHOW)[index==default_displayed]}"><small>{format_sentence_for_html(sentence)}</small></div>',
            indexes,
            sentences
        )
    ) + '<select id="translator" style="background-color:lightgoldenrodyellow;border:none">' + '\n'.join(
        map(
            lambda index: f'<option {(UNSELECTED,SELECTED)[index==default_displayed]} value="{index}">English Translation {index}</option>',
            indexes
        )
    ) + '</select>' + "</div>" + "<script>$('#translator').on('change', function () {" + '\n'.join(
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
    
def format_and_link_verses_for_html(verses:List[str],verses_to_display:List[str],scripture:str) -> str:
    return ' '.join(  
        "<p><small><a href= /{scripture}/{verse_address}>{verse}</a>  {verse_to_display}...</small></p>".format(
            scripture=scripture,
            verse_address=verse.replace(':','/'),
            verse=verse.replace('%20',' '),
            verse_to_display=text,
        ) for verse,text in zip(verses,verses_to_display)
    )

def format_sentence_for_html(sentence:str) -> str:
    return sentence.replace(",",",<br>").replace(";",";<br>").replace(
        ":",":<br>").replace("-","-<br>").replace("—","—<br>").replace(
        ".",".<br><br>").replace("!","!<br><br>").replace("?","?<br><br>")