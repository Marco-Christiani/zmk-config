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
        let pre = document.getElementsByTagName("pre")[0] 
        pre.innerHTML = replaceAll(pre.innerHTML, word, s);
    } 
}
let layer_color = "red";
let layers = ["NAV","SWAP","NUMPAD", "SYMBOLS", "MEDIA", "RGB ", "BLUETOOTH"];
highlight(layers, layer_color);

let modifier_color = "blue";
let modifiers = ["LALT", "RALT", "LGUI", "RGUI", "RSHFT", "LSHFT", "LCTRL", "RCTRL"];
highlight(modifiers, modifier_color);

let control_color = "green"; // music controls
let controls = ["C_PREV", "C_NEXT", "C_MUTE", "C_PP", "C_VOL_DN", "C_VOL_UP"];
highlight(controls, control_color);
