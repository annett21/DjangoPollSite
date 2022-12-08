plus_choice_btn = document.getElementById('plus_choice');

function add_choice_input() {
    choice_input_rows = document.getElementsByClassName('row-choice-input');
    var last_choice_input = choice_input_rows[choice_input_rows.length - 1];
    var cloned_choice_input = last_choice_input.cloneNode(true)
    cloned_choice_input.lastElementChild.lastElementChild.value = ''
    last_choice_input.after(cloned_choice_input);
    if (choice_input_rows.length >= 5) {
        plus_choice_btn.remove()
    }
}

plus_choice_btn.addEventListener('click', add_choice_input);