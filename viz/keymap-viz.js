function escapeRegExp(string) {
  return string.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'); // $& means the whole matched string
}
function replaceAll(str, find, replace) {
  return str.replace(new RegExp(escapeRegExp(find), 'g'), replace);
}

function highlight(wordArr, color) {
    for (let i = 0; i < wordArr.length; i++) {
        word = wordArr[i];
        let s = `<span style='color: ${color}'>${word}</span>`;
        let td_list = document.getElementsByTagName("td");
        for (let j = 0; j < td_list.length; j++){
            td_list[j].innerHTML = replaceAll(td_list[j].innerHTML, word, s);
        }
    } 
}
window.onload = function() {
    let layer_color = "red";
    let layers = ["SWAP","NAV","NUMPAD", "SYMBOLS", "MEDIA", "RGB", "BLUETOOTH"];
    highlight(layers, layer_color);

    let modifier_color = "blue";
    let modifiers = ["LALT", "RALT", "LGUI", "RGUI", "RSHFT", "LSHFT", "LCTRL", "RCTRL"];
    highlight(modifiers, modifier_color);

    let control_color = "green"; // music controls
    let controls = ["C_PREV", "C_NEXT", "C_MUTE", "C_PP", "C_VOL_DN", "C_VOL_UP"];
    highlight(controls, control_color);
}