function CPF(value, event) {
    let newValue = value.replace(/[^0-9]/g, '');


    const aux = (index) => index == 2 || index == 5;

    // on delete key.
    if (!event.data) {
        return value;
    }

    return newValue.split('').map((v, i) => aux(i) ? v + '.' : (i == 8 ? v + '-' : v)).join('');
};

function create(htmlStr) {
    var elem = document.createElement('div');
    att = document.createAttribute("class");
    att.value = "modal";
    elem.setAttributeNode(att);
    att = document.createAttribute("id");
    att.value = "modal";
    elem.setAttributeNode(att);
    elem.innerHTML = htmlStr;
    return elem;
}