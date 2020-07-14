############   NATIVE IMPORTS  ###########################
from typing import List
############ INSTALLED IMPORTS ###########################
############   LOCAL IMPORTS   ###########################
##########################################################

def format_sentences_to_be_hidden_html(sentences:List[str],default_displayed:int) -> str:
    indexes = range(len(sentences))
    HIDE = 'none'
    SHOW = 'block'
    hide = "hide"
    show = "show"
    SELECTED = 'selected="selected"'
    UNSELECTED = ''
    return '\n'.join(
        map(
            lambda index,sentence:f'<div id="translation{index}" style="text-align:center; display:{(HIDE,SHOW)[index==default_displayed]}"><small>{format_sentence_for_html(sentence)}</small></div>',
            indexes,
            sentences
        )
    ) + '<select id="translator">' + '\n'.join(
        map(
            lambda index: f'<option {(UNSELECTED,SELECTED)[index==default_displayed]} value="{index}">English Translation {index}</option>',
            indexes
        )
    ) + '</select>' + "<script>$('#translator').on('change', function () {" + '\n'.join(
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