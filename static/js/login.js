function CPF(value, event) {
    let newValue = value.replace(/[^0-9]/g, '');


    const aux = (index) => index == 2 || index == 5;

    // on delete key.
    if (!event.data) {
        return value;
    }

    return newValue.split('').map((v, i) => aux(i) ? v + '.' : (i == 8 ? v + '-' : v)).join('');
};